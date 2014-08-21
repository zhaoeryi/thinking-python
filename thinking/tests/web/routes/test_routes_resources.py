from __future__ import print_function
from thinking.tests import base
import webob
from thinking.web.dummy_controller import DummyController
from routes import Mapper


class ResourcesTestCase(base.ThinkingTestCase):

    def test_resources_with_collection_action(self):
        member_name = "message" 
        collection_name = "messages"

        map = Mapper()
        map.resource(member_name, collection_name, collection={"rss": "GET"})
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/messages/rss", environ)
        self.assertDictEqual(match_dict, {'action': u'rss', 'controller': u'messages'})

    def test_resources_with_member_action(self):
        member_name = "message" 
        collection_name = "messages"

        map = Mapper()
        map.resource(member_name, collection_name, member={'mark':'POST'})
        environ = {"REQUEST_METHOD":"POST"}
        match_dict = map.match("/messages/123/mark", environ)
        self.assertDictEqual(match_dict, {'action': u'mark', 'controller': u'messages', 'id': u'123'})
       

    def test_resources_with_path_prefix(self):
        member_name = "message" 
        collection_name = "messages"

        map = Mapper()
        map.resource(member_name, collection_name, path_prefix="/category/{category_id}")
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/category/123/messages/456", environ)
        self.assertDictEqual(match_dict, {'action': u'show', 'controller': u'messages', 'category_id': u'123', 'id': u'456'})


    def test_resources_with_parent_resource(self):
        member_name = "ip" 
        collection_name = "ips"

        map = Mapper()
        map.resource(member_name, collection_name,
                            parent_resource=dict(member_name='server',
                                                 collection_name='servers'))
        
        # GET    /servers/123/ips
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/servers/123/ips", environ)
        self.assertDictEqual(match_dict, {'action': u'index', 'server_id': u'123', 'controller': u'ips'})
        
        # POST   /servers/123/ips
        environ = {"REQUEST_METHOD":"POST"}
        match_dict = map.match("/servers/123/ips", environ)
        self.assertDictEqual(match_dict, {'action': u'create', 'server_id': u'123', 'controller': u'ips'})
        
        # GET    /servers/123/ips/new
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/servers/123/ips/new", environ)
        self.assertDictEqual(match_dict, {'action': u'new', 'server_id': u'123', 'controller': u'ips'})
        
        # PUT    /servers/123/ips/456
        environ = {"REQUEST_METHOD":"PUT"}
        match_dict = map.match("/servers/123/ips/456", environ)
        self.assertDictEqual(match_dict, {'action': u'update', 'server_id': u'123', 'controller': u'ips', 'id': u'456'})
        
        
        # DELETE /servers/123/ips/456
        environ = {"REQUEST_METHOD":"DELETE"}
        match_dict = map.match("/servers/123/ips/456", environ)
        self.assertDictEqual(match_dict, {'action': u'delete', 'server_id': u'123', 'controller': u'ips', 'id': u'456'})
        
        # GET    /servers/123/ips/456
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/servers/123/ips/456", environ)
        self.assertDictEqual(match_dict, {'action': u'show', 'server_id': u'123', 'controller': u'ips', 'id': u'456'})
        
        # GET    /servers/123/ips/456/edit
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/servers/123/ips/456/edit", environ)
        self.assertDictEqual(match_dict, {'action': u'edit', 'server_id': u'123', 'controller': u'ips', 'id': u'456'})
        
        # GET    /servers/123/ips.{format}
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/servers/123/ips.mp3", environ)
        self.assertDictEqual(match_dict, {'action': u'index', 'server_id': u'123', 'controller': u'ips', 'format': u'mp3'})
        
        # GET    /servers/123/ips/new.mp3
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/servers/123/ips/new.mp3", environ)
        self.assertDictEqual(match_dict, {'action': u'new', 'server_id': u'123', 'controller': u'ips', 'format': u'mp3'})
        
        # GET    /servers/123/ips/456.mp3
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/servers/123/ips/456.mp3", environ)
        self.assertDictEqual(match_dict, {'action': u'show', 'server_id': u'123', 'controller': u'ips', 'id': u'456', 'format': u'mp3'})
        
        print(match_dict)
        
    def test_resources_basic(self):
        member_name = "message" 
        collection_name = "messages"

        map = Mapper()
        map.resource(member_name, collection_name)
        
        '''
        This establishes the following convention:
        GET    /messages        => messages.index()    => url("messages")
        POST   /messages        => messages.create()   => url("messages")
        GET    /messages/new    => messages.new()      => url("new_message")
        PUT    /messages/1      => messages.update(id) => url("message", id=1)
        DELETE /messages/1      => messages.delete(id) => url("message", id=1)
        GET    /messages/1      => messages.show(id)   => url("message", id=1)
        GET    /messages/1/edit => messages.edit(id)   => url("edit_message", id=1)
        '''
        
        # GET    /messages        => messages.index()    => url("messages")
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/messages", environ)
        self.assertDictEqual(match_dict, {'action': u'index', 'controller': u'messages'})
        
        # POST   /messages        => messages.create()   => url("messages")
        environ = {"REQUEST_METHOD":"POST"}
        match_dict = map.match("/messages", environ)
        self.assertDictEqual(match_dict, {'action': u'create', 'controller': u'messages'})

        # GET    /messages/new    => messages.new()      => url("new_message")
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/messages/new", environ)
        self.assertDictEqual(match_dict, {'action': u'new', 'controller': u'messages'})
        
        # PUT    /messages/1      => messages.update(id) => url("message", id=1)
        environ = {"REQUEST_METHOD":"PUT"}
        match_dict = map.match("/messages/1", environ)
        self.assertDictEqual(match_dict, {'action': u'update', 'controller': u'messages', 'id': u'1'})
        
        # DELETE /messages/1      => messages.delete(id) => url("message", id=1)
        environ = {"REQUEST_METHOD":"DELETE"}
        match_dict = map.match("/messages/1", environ)
        self.assertDictEqual(match_dict, {'action': u'delete', 'controller': u'messages', 'id': u'1'})
        
        # GET    /messages/1      => messages.show(id)   => url("message", id=1)
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/messages/1", environ)
        self.assertDictEqual(match_dict, {'action': u'show', 'controller': u'messages', 'id': u'1'})
        
        # GET    /messages/1/edit => messages.edit(id)   => url("edit_message", id=1)
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/messages/1/edit", environ)
        self.assertDictEqual(match_dict, {'action': u'edit', 'controller': u'messages', 'id': u'1'})
        
        # GET    /messages.{format} => messages.edit(id)
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/messages.mp3", environ)
        self.assertDictEqual(match_dict, {'action': u'index', 'controller': u'messages', 'format': u'mp3'})
        
        # GET    /messages/new.{format}    => messages.new()
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/messages/new.mp3", environ)
        self.assertDictEqual(match_dict, {'action': u'new', 'controller': u'messages', 'format': u'mp3'})
        
        # GET    /messages/{id}.{format} => messages.show(id)
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/messages/1.mp3", environ)
        self.assertDictEqual(match_dict, {'action': u'show', 'controller': u'messages', 'id': u'1', 'format': u'mp3'})
