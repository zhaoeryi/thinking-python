#!/usr/bin/env bash

# Clean up the remainder of the screen processes
SCREEN=$(which screen)
if [[ -n "$SCREEN" ]]; then
    SESSION=$(screen -ls | awk '/[0-9].stack/ { print $1 }')
    if [[ -n "$SESSION" ]]; then
	for sess in "$SESSION"; do
           screen -X -S $sess quit
	done
    fi
fi

TOP_DIR=$(cd $(dirname "$0") && pwd)

# create a new named screen to run processes in
screen -d -m -S stack -t stack -s /bin/bash
sleep 1
# set a reasonable statusbar
screen -r stack -X hardstatus alwayslastline "$SCREEN_HARDSTATUS"

SERVICE_TIMEOUT=${SERVICE_TIMEOUT:-60}

# Specify which services to launch.  These generally correspond to
# screen tabs. If you like to add other services that are not enabled
# by default you can append them in your ENABLED_SERVICES variable in
# your localrc. For example for swift you can just add this in your
# localrc to add it with the other services:
# ENABLED_SERVICES="$ENABLED_SERVICES,swift"
# ENABLED_SERVICES=g-api,g-reg,key,n-api,n-crt,n-obj,n-cpu,n-net,n-vol,n-sch,n-novnc,n-xvnc,n-cauth,horizon,mysql,rabbit

ENABLED_SERVICES=rabbit,mysql,key,g-api,g-reg,key,n-api,n-crt,n-obj,n-cpu,n-cond,n-sch,n-novnc,n-xvnc,n-cauth,horizon,tempest,q-svc,q-agt,q-dhcp,q-l3,q-meta


# is_service_enabled() checks if the service(s) specified as arguments are
# enabled by the user in **ENABLED_SERVICES**.
#
# If there are multiple services specified as arguments the test performs a
# boolean OR or if any of the services specified on the command line
# return true.
#
# There is a special cases for some 'catch-all' services::
#   **nova** returns true if any service enabled start with **n-**
#   **glance** returns true if any service enabled start with **g-**
#   **neutron** returns true if any service enabled start with **q-**
function is_service_enabled() {
    services=$@
    for service in ${services}; do
        [[ ,${ENABLED_SERVICES}, =~ ,${service}, ]] && return 0
        [[ ${service} == "nova" && ${ENABLED_SERVICES} =~ "n-" ]] && return 0
        [[ ${service} == "glance" && ${ENABLED_SERVICES} =~ "g-" ]] && return 0
        [[ ${service} == "neutron" && ${ENABLED_SERVICES} =~ "q-" ]] && return 0
    done
    return 1
}

DEST=${DEST:-/opt/stack}

# Set the destination directories for openstack projects
NOVA_DIR=$DEST/nova
HORIZON_DIR=$DEST/horizon
GLANCE_DIR=$DEST/glance
GLANCECLIENT_DIR=$DEST/python-glanceclient
KEYSTONE_DIR=$DEST/keystone
NOVACLIENT_DIR=$DEST/python-novaclient
KEYSTONECLIENT_DIR=$DEST/python-keystoneclient
OPENSTACKCLIENT_DIR=$DEST/python-openstackclient
NOVNC_DIR=$DEST/noVNC
SWIFT_DIR=$DEST/swift
SWIFT3_DIR=$DEST/swift3
neutron_DIR=$DEST/neutron
neutron_CLIENT_DIR=$DEST/python-neutronclient
MELANGE_DIR=$DEST/melange
MELANGECLIENT_DIR=$DEST/python-melangeclient

# By default the location of swift drives and objects is located inside
# the swift source directory. SWIFT_DATA_DIR variable allow you to redefine
# this.
SWIFT_DATA_DIR=${SWIFT_DATA_DIR:-${DEST}/data/swift}

# We are going to have the configuration files inside the source
# directory, change SWIFT_CONFIG_DIR if you want to adjust that.
SWIFT_CONFIG_DIR=${SWIFT_CONFIG_DIR:-/etc/swift}

# devstack will create a loop-back disk formatted as XFS to store the
# swift data. By default the disk size is 1 gigabyte. The variable
# SWIFT_LOOPBACK_DISK_SIZE specified in bytes allow you to change
# that.
SWIFT_LOOPBACK_DISK_SIZE=${SWIFT_LOOPBACK_DISK_SIZE:-1000000}

# The ring uses a configurable number of bits from a path’s MD5 hash as
# a partition index that designates a device. The number of bits kept
# from the hash is known as the partition power, and 2 to the partition
# power indicates the partition count. Partitioning the full MD5 hash
# ring allows other parts of the cluster to work in batches of items at
# once which ends up either more efficient or at least less complex than
# working with each item separately or the entire cluster all at once.
# By default we define 9 for the partition count (which mean 512).
SWIFT_PARTITION_POWER_SIZE=${SWIFT_PARTITION_POWER_SIZE:-9}

# This variable allows you to configure how many replicas you want to be
# configured for your Swift cluster.  By default the three replicas would need a
# bit of IO and Memory on a VM you may want to lower that to 1 if you want to do
# only some quick testing.
SWIFT_REPLICAS=${SWIFT_REPLICAS:-3}

if is_service_enabled swift; then
    # If we are using swift, we can default the s3 port to swift instead
    # of nova-objectstore
    S3_SERVICE_PORT=${S3_SERVICE_PORT:-8080}
fi

# Set default port for nova-objectstore
S3_SERVICE_PORT=${S3_SERVICE_PORT:-3333}

# Set the tenant for service accounts in Keystone
SERVICE_TENANT_NAME=${SERVICE_TENANT_NAME:-service}

HOST_IP=127.0.0.1

SERVICE_HOST=${SERVICE_HOST:-$HOST_IP}

# Glance connection info.  Note the port must be specified.
GLANCE_HOSTPORT=${GLANCE_HOSTPORT:-$SERVICE_HOST:9292}

# Set Keystone interface configuration
KEYSTONE_API_PORT=${KEYSTONE_API_PORT:-5000}
KEYSTONE_AUTH_HOST=${KEYSTONE_AUTH_HOST:-$SERVICE_HOST}
KEYSTONE_AUTH_PORT=${KEYSTONE_AUTH_PORT:-35357}
KEYSTONE_AUTH_PROTOCOL=${KEYSTONE_AUTH_PROTOCOL:-http}
KEYSTONE_SERVICE_HOST=${KEYSTONE_SERVICE_HOST:-$SERVICE_HOST}
KEYSTONE_SERVICE_PORT=${KEYSTONE_SERVICE_PORT:-5000}
KEYSTONE_SERVICE_PROTOCOL=${KEYSTONE_SERVICE_PROTOCOL:-http}

# Our screenrc file builder
function screen_rc {
    SCREENRC=$TOP_DIR/stack-screenrc
    if [[ ! -e $SCREENRC ]]; then
        # Name the screen session
        echo "sessionname stack" > $SCREENRC
        # Set a reasonable statusbar
        echo "hardstatus alwayslastline '$SCREEN_HARDSTATUS'" >> $SCREENRC
        echo "screen -t stack bash" >> $SCREENRC
    fi
    # If this service doesn't already exist in the screenrc file
    if ! grep $1 $SCREENRC 2>&1 > /dev/null; then
        NL=`echo -ne '\015'`
        echo "screen -t $1 bash" >> $SCREENRC
        echo "stuff \"$2$NL\"" >> $SCREENRC
    fi
    rm $SCREENRC
}

# Our screen helper to launch a service in a hidden named screen
function screen_it {
    NL=`echo -ne '\015'`
    if is_service_enabled $1; then
        echo Starting $1 ... 
        # Append the service to the screen rc file
        screen_rc "$1" "$2"

        screen -S stack -X screen -t $1
        # sleep to allow bash to be ready to be send the command - we are
        # creating a new window in screen and then sends characters, so if
        # bash isn't running by the time we send the command, nothing happens
        sleep 1.5

        if [[ -n ${SCREEN_LOGDIR} ]]; then
            screen -S stack -p $1 -X logfile ${SCREEN_LOGDIR}/screen-${1}.${CURRENT_LOG_TIME}.log
            screen -S stack -p $1 -X log on
            ln -sf ${SCREEN_LOGDIR}/screen-${1}.${CURRENT_LOG_TIME}.log ${SCREEN_LOGDIR}/screen-${1}.log
        fi
        screen -S stack -p $1 -X stuff "$2$NL"
    fi
}

# KeyStone
screen_it key 'cd /opt/stack/keystone && /opt/stack/keystone/bin/keystone-all --config-file /etc/keystone/keystone.conf --debug'

# Glance
screen_it g-reg 'cd /opt/stack/glance; /usr/local/bin/glance-registry --config-file=/etc/glance/glance-registry.conf'
screen_it g-api 'cd /opt/stack/glance; /usr/local/bin/glance-api --config-file=/etc/glance/glance-api.conf'

# Nova
screen_it n-api 'cd /opt/stack/nova && /usr/local/bin/nova-api'
screen_it n-cpu 'cd /opt/stack/nova && sg libvirtd '\''/usr/local/bin/nova-compute --config-file /etc/nova/nova.conf'\'''
screen_it n-cond 'cd /opt/stack/nova && /usr/local/bin/nova-conductor --config-file /etc/nova/nova.conf'
screen_it n-cell-region 'cd /opt/stack/nova && /usr/local/bin/nova-cells --config-file /etc/nova/nova.conf'
screen_it n-cell-child 'cd /opt/stack/nova && /usr/local/bin/nova-cells --config-file /etc/nova/nova.conf'
screen_it n-crt 'cd /opt/stack/nova && /usr/local/bin/nova-cert --config-file /etc/nova/nova.conf'
screen_it n-net 'cd /opt/stack/nova && /usr/local/bin/nova-network --config-file /etc/nova/nova.conf'
screen_it n-sch 'cd /opt/stack/nova && /usr/local/bin/nova-scheduler --config-file /etc/nova/nova.conf'
screen_it n-api-meta 'cd /opt/stack/nova && /usr/local/bin/nova-api-metadata --config-file /etc/nova/nova.conf'
screen_it n-novnc 'cd /opt/stack/nova && /usr/local/bin/nova-novncproxy --config-file /etc/nova/nova.conf --web /opt/stack/noVNC'
screen_it n-xvnc 'cd /opt/stack/nova && /usr/local/bin/nova-xvpvncproxy --config-file /etc/nova/nova.conf'
screen_it n-spice 'cd /opt/stack/nova && /usr/local/bin/nova-spicehtml5proxy --config-file /etc/nova/nova.conf --web '
screen_it n-cauth 'cd /opt/stack/nova && /usr/local/bin/nova-consoleauth --config-file /etc/nova/nova.conf'
screen_it n-obj 'cd /opt/stack/nova && /usr/local/bin/nova-objectstore --config-file /etc/nova/nova.conf'

# Cinder
screen_it c-api 'cd /opt/stack/cinder && /usr/local/bin/cinder-api --config-file /etc/cinder/cinder.conf'
screen_it c-sch 'cd /opt/stack/cinder && /usr/local/bin/cinder-scheduler --config-file /etc/cinder/cinder.conf'
screen_it c-bak 'cd /opt/stack/cinder && /usr/local/bin/cinder-backup --config-file /etc/cinder/cinder.conf'
screen_it c-vol 'cd /opt/stack/cinder && /usr/local/bin/cinder-volume --config-file /etc/cinder/cinder.conf'

# Neutron
#screen_it q-svc 'cd /opt/stack/neutron && python /usr/local/bin/neutron-server --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/openvswitch/ovs_neutron_plugin.ini'

#screen_it q-agt 'cd /opt/stack/neutron && python /usr/local/bin/neutron-openvswitch-agent --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/openvswitch/ovs_neutron_plugin.ini'

#screen_it q-dhcp 'cd /opt/stack/neutron && python /usr/local/bin/neutron-dhcp-agent --config-file /etc/neutron/neutron.conf --config-file=/etc/neutron/dhcp_agent.ini'

#screen_it q-l3 'cd /opt/stack/neutron && python /usr/local/bin/neutron-l3-agent --config-file /etc/neutron/neutron.conf --config-file=/etc/neutron/l3_agent.ini'

#screen_it q-meta 'cd /opt/stack/neutron && python /usr/local/bin/neutron-metadata-agent --config-file /etc/neutron/neutron.conf --config-file=/etc/neutron/metadata_agent.ini'

# Horizon
screen_it horizon 'cd /opt/stack/horizon && sudo tail -f /var/log/apache2/horizon_error.log'

