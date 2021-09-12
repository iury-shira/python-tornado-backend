import tornado.web
import tornado.ioloop

import json

class BasicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello from Python Tornado server!")


class HtmlRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class QueryRequestHandler(tornado.web.RequestHandler):
    def get(self):
        jojo = self.get_argument("jojo").lower()

        if jojo in set(get_jojos("list.txt")):
            self.write("Your query has a valid jojo!")
        else:
            self.write("Invalid jojo!")


class ResourceRequestHandler(tornado.web.RequestHandler):
    def get(self, jojo: str, part: int):
        self.write(f"So you would like to see {jojo} in part {part}?")


class ListRequetHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(get_jojos("list.txt")))

    def post(self):
        jojo = self.get_argument("jojo").lower()

        if jojo in set(get_jojos("list.txt")):
            self.write(json.dumps({"message": "we already have this jojo!"}))
        else:
            with open("list.txt", "a") as list:
                list.write(f"\n{jojo}")

            self.write(json.dumps({"message": f"{jojo} added successfully to jojo list!"}))


def get_jojos(filename: str) -> list:
    with open(filename, "r") as list:
            return list.read().split('\n')


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", BasicRequestHandler),
        (r"/html", HtmlRequestHandler),
        (r"/query", QueryRequestHandler),
        (r"/resource/([a-z]+)/([0-9]+)", ResourceRequestHandler),
        (r"/list", ListRequetHandler)
    ])

    port = 8080
    app.listen(port)

    print(f"Python Tornado server listening on port {port}...")
    tornado.ioloop.IOLoop.current().start()
