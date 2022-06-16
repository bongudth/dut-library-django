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
            self.favourite[book_id] = {'get_absolute_url': book.get_absolute_url(), 'title': book.title, 'author': book.author, 'description': book.description, 'image_url': book.image_url}

        self.session.modified = True

    def __len__(self):
        return len(self.favourite)
