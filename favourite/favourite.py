class Favourite:
    def __init__(self, request):
        self.session = request.session
        favourite = self.session.get('skey')
        if 'skey' not in request.session:
            favourite = self.session['skey'] = {}
        self.favourite = favourite

    def add(self, book):
        book_id = book.id

        if book_id not in self.favourite:
            self.favourite[book_id] = {'title': book.title}

        self.session.modified = True
