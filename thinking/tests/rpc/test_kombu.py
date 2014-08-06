# coding=utf-8
# http://blog.csdn.net/hackerain/article/details/7875614
from __future__ import print_function

import kombu
import time

from thinking.tests import base


class KombuTestCase(base.ThinkingTestCase):   

    def setUp(self):
       
        self._hack_conn = kombu.connection.BrokerConnection('amqp://guest:guest@127.0.0.1:5672//')
        self._hack_channel = self._hack_conn.channel()

        # 定义了一个 topic 类型的 exchange
        self._hack_topic_exchange = kombu.entity.Exchange(name='hack_exchange',
                                              type='topic')        
        
        # 在这里进行了exchange和queue的绑定，并且指定了这个queue的routing_key
        # OpenStack中, 由 Consumer 负责创建Queue, 并且要在Producer发送之前就创建好
        # see nova.openstack.common.rpc.impl_kombu.ConsumerBase
        self._hack_queue = kombu.entity.Queue(channel=self._hack_channel,
                                   exchange=self._hack_topic_exchange,
                                   name='hack_queue',
                                   routing_key='hack_routing_key')
        self._hack_queue.declare()
        
        super(KombuTestCase, self).setUp()

    def tearDown(self):
        if self._hack_conn:
            try:
                self._hack_conn.release()
            except self.connection_errors:
                pass
            # Setting this in case the next statement fails, though
            # it shouldn't be doing any network operations, yet.
            self._hack_conn = None
        super(KombuTestCase, self).tearDown()
                
    def _consume_by_queue(self):
        def _callback(raw_message):
            message = self._hack_channel.message_to_python(raw_message)
            try:
                print("Consume message by queue: ", message.payload)
            except Exception:
                LOG.exception(_("Failed to process message... skipping it."))
            finally:
                message.ack()
        self._hack_queue.consume(callback=_callback)
        self._hack_conn.drain_events()   
        
    def _consume_by_consumer(self):
        def _callback(raw_message):
            message = self._hack_channel.message_to_python(raw_message)
            try:
                print("Consume message by consumer: ", message.payload)
            except Exception:
                LOG.exception(_("Failed to process message... skipping it."))
            finally:
                message.ack()        
        self._hack_channel.basic_consume(callback=_callback)  
        
        consumer = kombu.messaging.Consumer(self._hack_channel, self._hack_queue)  
        consumer.register_callback(_callback)  
        consumer.consume()
        
        self._hack_conn.drain_events()   

    def _produce(self):
        # producer
        
        msg_content = str(time.clock())
        print "Publish message: ", msg_content
        producer = kombu.messaging.Producer(exchange=self._hack_topic_exchange,
                                                 channel=self._hack_channel,
                                                 routing_key='hack_routing_key')
        producer.publish(msg_content)
        
    def test_consume_by_queue(self):
        # consumer
        self._produce()
        self._consume_by_queue()
        
        # consumer
        self._produce()
        self._consume_by_queue()        

    def test_consume_by_consumer(self):
        # consumer
        self._produce()
        self._consume_by_consumer()
        
        # consumer
        self._produce()
        self._consume_by_consumer()        
