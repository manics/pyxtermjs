"""A single common terminal for all websockets.
"""
import argparse
import os.path
import shlex
import sys
import terminado
from terminado import TermSocket, SingleTermManager
import tornado.ioloop
import tornado.log
import tornado.options
import tornado.web

__version__ = "0.1.0"
STATIC_DIR = os.path.join(os.path.dirname(terminado.__file__), "_static")
STATIC_APP_DIR = os.path.join(os.path.dirname(__file__), "static")
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


# https://stackoverflow.com/a/10165739
class TerminalPageHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render(
            "index.html",
            terminado_static=self.settings["terminado_static"],
            app_static=self.settings["app_static"],
            ws_url_path="websocket",
        )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Terminado browser terminal",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-p", "--port", default=5000, help="port to run server on")
    parser.add_argument(
        "--host",
        "--ip",
        default="127.0.0.1",
        help="host to run server on (use 0.0.0.0 to allow access from other hosts)",
    )
    parser.add_argument("--debug", action="store_true", help="debug the server")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    parser.add_argument(
        "--command", default="bash", help="Command to run in the terminal"
    )
    parser.add_argument(
        "--cmd-args",
        default="",
        help="arguments to pass to command (i.e. --cmd-args='arg1 arg2 --flag')",
    )
    parser.add_argument(
        "--baseurl",
        default=os.getenv("JUPYTERHUB_SERVICE_PREFIX", "/"),
        help="run server under this base-url (/prefix)",
    )

    # If this is run in place of jupyter-* we may receive some standard jupyter args
    args, other = parser.parse_known_args(argv)
    if args.version:
        print(__version__)
        sys.exit(0)
    if other:
        print(f"Ignoring arguments {other}")

    shell_command = [args.command] + shlex.split(args.cmd_args)
    baseurl = args.baseurl.rstrip("/")
    print(f"Serving on http://{args.host}:{args.port}{baseurl}/")

    term_manager = SingleTermManager(shell_command=shell_command)
    handlers = [
        (f"{baseurl}/websocket", TermSocket, {"term_manager": term_manager}),
        (fr"{baseurl}/", TerminalPageHandler),
        (
            fr"{baseurl}/terminado-static/(.*)",
            tornado.web.StaticFileHandler,
            {"path": STATIC_DIR},
        ),
        (
            fr"{baseurl}/app-static/(.*)",
            tornado.web.StaticFileHandler,
            {"path": STATIC_APP_DIR},
        ),
    ]
    if baseurl:
        # Handle /baseurl without trailing /
        handlers.append(
            (
                f"{baseurl}",
                tornado.web.RedirectHandler,
                {"url": f"{baseurl}/", "permanent": False},
            )
        )

    if args.debug:
        tornado.options.options.logging = "debug"
    tornado.log.enable_pretty_logging()
    # tornado.log.app_log.debug('test debug message')

    app = tornado.web.Application(
        handlers,
        static_path=STATIC_DIR,
        template_path=TEMPLATE_DIR,
        terminado_static=lambda path: f"{baseurl}/terminado-static/path",
        # https://github.com/takluyver/tornado_xstatic/blob/d9499b57c1291764debcc2be299c12d7b3dce7d3/tornado_xstatic.py#L58-L66
        app_static=lambda path: f"{baseurl}/app-static/{path}",
        debug=args.debug,
    )
    app.listen(args.port, args.host)
    loop = tornado.ioloop.IOLoop.instance()
    try:
        loop.start()
    except KeyboardInterrupt:
        print(" Shutting down on SIGINT")
    finally:
        term_manager.shutdown()
        loop.close()


if __name__ == "__main__":
    main(sys.argv)
