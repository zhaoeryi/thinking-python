from __future__ import print_function

import json
import logging
import routes.middleware
import webob
import webob.dec
import webob.exc

LOG = logging.getLogger(__name__)


class MyResource():
    def __init__(self, controller):
        self.controller = controller

    def _get_method(self, request, action, content_type, body):
        """Look up the action-specific method and its extensions."""

        # Look up the method
        try:
            if not self.controller:
                meth = getattr(self, action)
            else:
                meth = getattr(self.controller, action)
        except AttributeError:
                raise
        else:
            return meth

    def get_action_args(self, request_environment):
        """Parse dictionary created by routes library."""

        # NOTE(Vek): Check for get_action_args() override in the
        # controller
        if hasattr(self.controller, 'get_action_args'):
            return self.controller.get_action_args(request_environment)

        try:
            args = request_environment['wsgiorg.routing_args'][1].copy()
        except (KeyError, IndexError, AttributeError):
            return {}

        try:
            del args['controller']
        except KeyError:
            pass

        try:
            del args['format']
        except KeyError:
            pass

        return args

    def dispatch(self, method, request, action_args):
        """Dispatch a call to the action-specific method."""
        return method(req=request, **action_args)

    def _process_stack(self, request, action, action_args,
                       content_type, body):
        """Implement the processing stack."""

        # Get the implementing method
        try:
            meth = self._get_method(request, action, content_type, body)
        except (AttributeError, TypeError):
            return webob.exc.HTTPNotFound()
        except KeyError as ex:
            msg = _("There is no such action: %s") % ex.args[0]
            return webob.exc.HTTPBadRequest(explanation=msg)

        # Update the action args
        if body:
            contents = {'body': body}
            action_args.update(contents)

        response = self.dispatch(meth, request, action_args)
        return response

    @webob.dec.wsgify(RequestClass=webob.Request)
    def __call__(self, request):
        """WSGI method that controls (de)serialization and method dispatch."""
        # Identify the action, its arguments, and the requested
        # content type
        action_args = self.get_action_args(request.environ)
        action = action_args.pop('action', None)
        if request.body:
            body = json.loads(request.body)
        else:
            body = None
        # NOTE(Vek): Splitting the function up this way allows for
        #            auditing by external tools that wrap the existing
        #            function.  If we try to audit __call__(), we can
        #            run into troubles due to the @webob.dec.wsgify()
        #            decorator.
        return self._process_stack(request, action, action_args,
                               request.content_type, body)


# app
class MyRouter():

    """WSGI middleware that maps incoming requests to WSGI apps."""

    def __init__(self, mapper):
        """Create a router for the given routes.Mapper.

        Each route in `mapper` must specify a 'controller', which is a
        WSGI app to call.  You'll probably want to specify an 'action' as
        well and have your controller be an object that can route
        the request to the action-specific method.

        Examples:
          mapper = routes.Mapper()
          sc = ServerController()

          # Explicit mapping of one route to a controller+action
          mapper.connect(None, '/svrlist', controller=sc, action='list')

          # Actions are all implicitly defined
          mapper.resource('server', 'servers', controller=sc)

          # Pointing to an arbitrary WSGI app.  You can specify the
          # {path_info:.*} parameter so the target app can be handed just that
          # section of the URL.
          mapper.connect(None, '/v1.0/{path_info:.*}', controller=BlogApp())

        """
        self.map = mapper
        self._router = routes.middleware.RoutesMiddleware(self._dispatch,
                                                          self.map)

    @webob.dec.wsgify(RequestClass=webob.Request)
    def __call__(self, req):
        """Route the incoming request to a controller based on self.map.

        If no match, return a 404.

        """
        return self._router

    @staticmethod
    @webob.dec.wsgify(RequestClass=webob.Request)
    def _dispatch(req):
        """Dispatch the request to the appropriate controller.

        Called by self._router after matching the incoming request to a route
        and putting the information into req.environ.  Either returns 404
        or the routed WSGI app's response.

        """
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            return webob.exc.HTTPNotFound()
        app = match['controller']
        return app
