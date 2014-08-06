import json
import routes
from thinking.routes import MyResource
from thinking.routes import MyRouter
from thinking.tests import base
import webob


class ServerController(object):
    def create(self, req, body):
        return "ServerController.create"

    def delete(self, req, id):
        """Destroys a server."""
        return "ServerController.delete(%s)" % id

    def index(self, req):
        """Returns a list of server names and ids for a given user."""
        return "ServerController.index"

    def show(self, req, id):
        """Returns server details by server id."""
        return "ServerController.show(%s)" % id

    def update(self, req, id, body):
        """Update server then pass on to version-specific controller."""
        return "ServerController.update(%s)" % id

    def my_action(self, req):
        return "ServerController.my_action"


class VolumeController(object):
    def create(self, req, server_id, body):
        return "VolumeController.create"

    def index(self, req, server_id):
        """Returns the list of volume attachments for a given instance."""
        return "VolumeController.index"

    def show(self, req, server_id, id):
        """Return data about the given volume."""
        return "VolumeController.show"

    def update(self, req, server_id, id, body):
        return "VolumeController.update"

    def delete(self, req, server_id, id):
        """Detach a volume from an instance."""
        return "VolumeController.delete"


class ResourceMapperTestCase(base.ThinkingTestCase):

    def setUp(self):
        """
        GET    /servers         => servers.index()
        POST   /servers         => servers.create()
        GET    /servers/my_action  => servers.my_action()
        GET    /servers/new     => servers.new()
        PUT    /servers/id      => servers.update(id)
        DELETE /servers/id      => servers.delete(id)
        GET    /servers/id      => servers.show(id)

        ServerController is parent of VolumeController (reference at VolumeAttachmentController)
        http://docs.rackspace.com/servers/api/v2/cs-devguide/content/Volume_Attachment_Actions.html
        """
        self.mapper = routes.Mapper()
        self.mapper.resource("server", "servers",
                        controller=MyResource(ServerController()),
                        collection={'my_action': 'GET'},
                        member={'action': 'POST'})

        self.mapper.resource('volumes', 'volumes',
                             controller=MyResource(VolumeController()),
                             parent_resource=dict(member_name='server',
                                                 collection_name='servers'))

        self.router = MyRouter(self.mapper)
        # print self.mapper
        super(ResourceMapperTestCase, self).setUp()

    def test_server_create(self):
        # invoke ServerController.create
        req = webob.Request.blank('/servers')
        req.method = 'POST'
        req.content_type = 'application/json'
        req.body = json.dumps({
            'fakebody': {
                'host': 'hostname',
                'block_migration': False,
                'disk_over_commit': False,
            }
        })

        response = req.get_response(self.router)
        self.assertEqual(response.body, "ServerController.create")

    def test_server_delete(self):
        id = 12345
        # invoke ServerController.delete
        req = webob.Request.blank('/servers/%s' % id)
        req.method = 'DELETE'
        req.content_type = 'application/json'

        response = req.get_response(self.router)
        self.assertEqual(response.body, "ServerController.delete(%s)" % id)

    def test_server_myaction(self):
        # invoke ServerController.my_action
        req = webob.Request.blank('/servers/my_action')
        req.method = 'GET'
        req.content_type = 'application/json'

        response = req.get_response(self.router)
        self.assertEqual(response.body, "ServerController.my_action")

    def test_server_index(self):
        # invoke ServerController.index
        req = webob.Request.blank('/servers')
        req.method = 'GET'
        req.content_type = 'application/json'

        response = req.get_response(self.router)
        self.assertEqual(response.body, "ServerController.index")

    def test_server_update(self):
        id = 12345
        # invoke ServerController.update
        req = webob.Request.blank('/servers/%s' % id)
        req.method = 'PUT'
        req.content_type = 'application/json'
        req.body = json.dumps({
            'fakebody': {
                'host': 'hostname',
                'block_migration': False,
                'disk_over_commit': False,
            }
        })
        response = req.get_response(self.router)
        self.assertEqual(response.body, "ServerController.update(%s)" % id)

    def test_volume_create(self):
        # invoke VolumeController.create
        req = webob.Request.blank('/servers/123/volumes')
        req.method = 'POST'
        req.content_type = 'application/json'
        req.body = json.dumps({
            'fakebody': {
                'host': 'hostname',
                'block_migration': False,
                'disk_over_commit': False,
            }
        })

        response = req.get_response(self.router)
        self.assertEqual(response.body, "VolumeController.create")

    def test_volume_index(self):
        # invoke VolumeController.index
        req = webob.Request.blank('/servers/123/volumes')
        req.method = 'GET'
        req.content_type = 'application/json'

        response = req.get_response(self.router)
        self.assertEqual(response.body, "VolumeController.index")

    def test_volume_show(self):
        # invoke VolumeController.show
        req = webob.Request.blank('/servers/123/volumes/456')
        req.method = 'GET'
        req.content_type = 'application/json'

        response = req.get_response(self.router)
        self.assertEqual(response.body, "VolumeController.show")

    def test_volume_update(self):
        # invoke VolumeController.update
        req = webob.Request.blank('/servers/123/volumes/456')
        req.method = 'PUT'
        req.content_type = 'application/json'
        req.body = json.dumps({
            'fakebody': {
                'host': 'hostname',
                'block_migration': False,
                'disk_over_commit': False,
            }
        })
        response = req.get_response(self.router)
        self.assertEqual(response.body, "VolumeController.update")

    def test_volume_delete(self):
        # invoke VolumeController.delete
        req = webob.Request.blank('/servers/123/volumes/456')
        req.method = 'DELETE'
        req.content_type = 'application/json'

        response = req.get_response(self.router)
        self.assertEqual(response.body, "VolumeController.delete")
