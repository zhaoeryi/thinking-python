import _hacking
import sys
import time
import kombu
import kombu.connection
import kombu.entity
import kombu.messaging

LOG = _hacking.logger

class Connection(object):
    """Connection object."""
    
    
    def __init__(self):
        self.consumers = []
        self.consumer_thread = None
        self.proxy_callbacks = []
        self.max_retries = 3
        self.interval_start = 1
        self.interval_stepping = 2
        self.interval_max = 30
        self.memory_transport = False

        params_list = []
        params = {'hostname': 'localhost',
                  'port': 5672,
                  'userid': 'guest',
                  'password': 'guest',
                  'virtual_host': '/'
        }
        
        params_list.append(params)
        self.params_list = params_list

        self.connection = None
        self.reconnect()    

    def reconnect(self):
        """Handles reconnecting and re-establishing queues.
        Will retry up to self.max_retries number of times.
        self.max_retries = 0 means to retry forever.
        Sleep between tries, starting at self.interval_start
        seconds, backing off self.interval_stepping number of seconds
        each attempt.
        """

        attempt = 0
        while True:
            params = self.params_list[attempt % len(self.params_list)]
            attempt += 1
            try:
                self._connect(params)
                return
            except Exception as e:
                # NOTE(comstud): Unfortunately it's possible for amqplib
                # to return an error not covered by its transport
                # connection_errors in the case of a timeout waiting for
                # a protocol response.  (See paste link in LP888621)
                # So, we check all exceptions for 'timeout' in them
                # and try to reconnect in this case.
                if 'timeout' not in str(e):
                    raise

            log_info = {}
            log_info['err_str'] = str(e)
            log_info['max_retries'] = self.max_retries
            log_info.update(params)

            if self.max_retries and attempt == self.max_retries:
                LOG.error(_('Unable to connect to AMQP server on '
                            '%(hostname)s:%(port)d after %(max_retries)d '
                            'tries: %(err_str)s') % log_info)
                # NOTE(comstud): Copied from original code.  There's
                # really no better recourse because if this was a queue we
                # need to consume on, we have no way to consume anymore.
                sys.exit(1)

            if attempt == 1:
                sleep_time = self.interval_start or 1
            elif attempt > 1:
                sleep_time += self.interval_stepping
            if self.interval_max:
                sleep_time = min(sleep_time, self.interval_max)

            log_info['sleep_time'] = sleep_time
            LOG.error(_('AMQP server on %(hostname)s:%(port)d is '
                        'unreachable: %(err_str)s. Trying again in '
                        '%(sleep_time)d seconds.') % log_info)
            time.sleep(sleep_time)
            
    def _connect(self, params):
        """Connect to rabbit.  Re-establish any queues that may have
        been declared before if we are reconnecting.  Exceptions should
        be handled by the caller.
        """
        if self.connection:
            LOG.info(_("Reconnecting to AMQP server on "
                     "%(hostname)s:%(port)d") % params)
            try:
                self.connection.release()
            except self.connection_errors:
                pass
            # Setting this in case the next statement fails, though
            # it shouldn't be doing any network operations, yet.
            self.connection = None
        self.connection = kombu.connection.BrokerConnection(**params)
        self.connection_errors = self.connection.connection_errors
        if self.memory_transport:
            # Kludge to speed up tests.
            self.connection.transport.polling_interval = 0.0
        self.connection.connect()
        self.channel = self.connection.channel()
        # work around 'memory' transport bug in 1.1.3
        if self.memory_transport:
            self.channel._new_queue('ae.undeliver')
        for consumer in self.consumers:
            consumer.reconnect(self.channel)
        LOG.info(('Connected to AMQP server on %(hostname)s:%(port)d') % 
                 params)
        
  
