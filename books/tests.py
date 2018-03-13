"""Books app feature tests."""

import factory
from django_common.auth_backends import User

from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from rest_framework import status
from rest_framework.test import APITestCase

from .models import (
    Author,
    Publisher,
    Book,
    Favourite,
    ReadingList,
)


class UserFactory(DjangoModelFactory):
    """Factory for users."""

    username = factory.Faker('name')

    class Meta:
        model = User


class AuthorFactory(DjangoModelFactory):
    """Factory for authors."""

    name = factory.Faker('name')
    description = factory.Faker('text')

    class Meta:
        model = Author


class PublisherFactory(DjangoModelFactory):
    """Factory for publishers."""

    name = factory.Faker('name')
    description = factory.Faker('text')

    class Meta:
        model = Publisher


class BookFactory(DjangoModelFactory):
    """Factory for books."""

    title = factory.Faker('name')
    genre = FuzzyChoice(c[0] for c in Book.GENRES)
    description = factory.Faker('text')
    pages = factory.Faker('random_int', min=0, max=9999)
    publisher = factory.SubFactory(PublisherFactory)
    published_date = factory.Faker('date_this_year')

    class Meta:
        model = Book

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        """Create authors that have been passed in."""
        if create and extracted:
            for author in extracted:
                self.authors.add(author)


class FavouriteFactory(DjangoModelFactory):
    """Factory for favourites."""

    book = factory.SubFactory(BookFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Favourite


class ReadingListFactory(DjangoModelFactory):
    """Reading list factory."""

    book = factory.SubFactory(BookFactory)
    started_reading = factory.Faker('boolean')
    started_date = factory.Faker('date_this_year')
    finished_reading = factory.Faker('boolean')
    finished_date = factory.Faker('date_this_year')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = ReadingList


class TestBookFunctionalTestCase(APITestCase):
    """Book model api functional tests."""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(is_superuser=True)
        cls.author = AuthorFactory()
        cls.publisher = PublisherFactory()
        cls.book = BookFactory(authors=[cls.author], publisher=cls.publisher)

    def test_listing_book_items(self):
        """Test that a user can read book items."""
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/books/book/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(self.book.id, response.data[0]['id'])
        self.assertEqual(self.book.title, response.data[0]['title'])
        self.assertEqual(self.book.genre, response.data[0]['genre'])
        self.assertEqual(self.book.description, response.data[0]['description'])
        self.assertEqual(self.book.pages, response.data[0]['pages'])
        self.assertEqual(self.author.id, response.data[0]['authors'][0]['id'])
        self.assertEqual(self.book.publisher.id, response.data[0]['publisher']['id'])
        self.assertEqual(self.book.published_date.strftime('%Y-%m-%d'), response.data[0]['published_date'])

    def test_creating_book_item(self):
        """Test that a user can create a book item."""
        new_book = BookFactory(authors=[self.author], publisher=self.publisher)
        self.client.force_authenticate(user=self.user)

        # clean book already created as part of factory
        Book.objects.get(id=new_book.id).delete()

        response = self.client.post(
            "/books/book/",
            data={
                "title": new_book.title,
                "genre": new_book.genre,
                "description": new_book.description,
                "pages": new_book.pages,
                "authors": [
                    {
                        "name": self.author.name,
                        "description": self.author.description,
                    }
                ],
                "publisher": {
                    "name": self.publisher.name,
                    "description": self.publisher.description,
                },
                "published_date": new_book.published_date,
            },
            format='json',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(new_book.title, response.data['title'])
        self.assertEqual(new_book.genre, response.data['genre'])
        self.assertEqual(new_book.description, response.data['description'])
        self.assertEqual(new_book.pages, response.data['pages'])
        self.assertEqual(new_book.published_date.strftime('%Y-%m-%d'), response.data['published_date'])

        # check that there are now two items in the books list
        response = self.client.get("/books/book/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEquals(2, len(response.data))

    def test_updating_book_item(self):
        """Test that a user can update a book item."""
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            "/books/book/{}/".format(self.book.id),
            data={
                "title": "New Book Title",
                "description": "New Book Description",
            },
            format='json',
        )

        # Retrieve the newly updated book item
        book = Book.objects.get(id=self.book.id)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(book.title, response.data['title'])
        self.assertEqual(book.genre, response.data['genre'])
        self.assertEqual(book.description, response.data['description'])

    def test_deleting_book_item(self):
        """Test that a user can delete a book item."""
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            "/books/book/{}/".format(self.book.id),
            format='json',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        # Retrieve the book list check that the list has no items
        response = self.client.get("/books/book/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEquals(0, len(response.data))


class TestReadingListFunctionalTestCase(APITestCase):
    """Reading list api functional tests."""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(is_superuser=True)
        cls.author = AuthorFactory()
        cls.publisher = PublisherFactory()
        cls.book = BookFactory(authors=[cls.author], publisher=cls.publisher)
        cls.reading_list = ReadingListFactory(book=cls.book, user=cls.user)

    def test_listing_reading_list_items(self):
        """Test that a user can view the reading list items."""
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/books/reading/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(self.reading_list.id, response.data[0]['id'])
        self.assertEqual(self.reading_list.book.id, response.data[0]['book'])
        self.assertEqual(self.reading_list.started_reading, response.data[0]['started_reading'])
        self.assertEqual(self.reading_list.started_date.strftime('%Y-%m-%d'), response.data[0]['started_date'])
        self.assertEqual(self.reading_list.finished_reading, response.data[0]['finished_reading'])
        self.assertEqual(self.reading_list.finished_date.strftime('%Y-%m-%d'), response.data[0]['finished_date'])
        self.assertEqual(self.reading_list.user.id, response.data[0]['user'])

    def test_creating_reading_list_item(self):
        """Test that a user can create a new reading list item."""
        new_list_item = ReadingListFactory(book=self.book, user=self.user)
        self.client.force_authenticate(user=self.user)

        # clean book already created as part of factory
        ReadingList.objects.get(id=new_list_item.id).delete()

        response = self.client.post(
            "/books/reading/",
            data={
                "book": new_list_item.book.id,
                "started_reading": new_list_item.started_reading,
                "finished_reading": new_list_item.finished_reading,
                "user": new_list_item.user.id,
            },
            format='json',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(new_list_item.book.id, response.data['book'])
        self.assertEqual(new_list_item.started_reading, response.data['started_reading'])
        self.assertEqual(new_list_item.finished_reading, response.data['finished_reading'])
        self.assertEqual(new_list_item.user.id, response.data['user'])

        # check that there are now two items in the books list
        response = self.client.get("/books/reading/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEquals(2, len(response.data))

    def test_deleting_reading_list_item(self):
        """Test that a user can delete a reading list item."""
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            "/books/reading/{}/".format(self.reading_list.id),
            format='json',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        # Retrieve the book list check that the list has no items
        response = self.client.get("/books/reading/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEquals(0, len(response.data))

    def test_another_user_cannot_view_or_edit_reading_list_items(self):
        """Test that another user cannot read the reading list items."""
        another_user = UserFactory()
        another_list_item = ReadingListFactory(book=self.book, user=self.user)
        self.client.force_authenticate(user=another_user)

        # Retrieve list of todos
        response = self.client.get("/books/reading/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        # List should be empty since the reading list previously created does not belong to this user
        self.assertEquals(0, len(response.data))

        response = self.client.post(
            "/books/reading/",
            data={
                "book": another_list_item.book.id,
                "started_reading": another_list_item.started_reading,
                "finished_reading": another_list_item.finished_reading,
                "user": another_list_item.user.id,
            },
            format='json',
        )

        # Should not be allowed to POST
        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        response = self.client.patch(
            "/books/reading/{}/".format(another_list_item.id),
            data={
                "finished_reading": True,
            },
            format='json',
        )

        # Should not be allowed to PATCH
        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Should not be allowed to DELETE
        response = self.client.delete(
            "/books/reading/{}/".format(another_list_item.id),
            format='json',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )


class TestFavouritesFunctionalTestCase(APITestCase):
    """Favourites api functional tests."""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(is_superuser=True)
        cls.book = BookFactory()
        cls.favourite = FavouriteFactory(book=cls.book, user=cls.user)

    def test_listing_favourites(self):
        """Test that a user can view the favourites."""
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/books/favourite/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(self.favourite.id, response.data[0]['id'])
        self.assertEqual(self.favourite.book.id, response.data[0]['book'])
        self.assertEqual(self.favourite.user.id, response.data[0]['user'])

    def test_creating_favourite_item(self):
        """Test that a user can create a new favourite item."""
        new_book = BookFactory()
        new_favorite = FavouriteFactory(book=new_book, user=self.user)
        self.client.force_authenticate(user=self.user)

        # clean book already created as part of factory
        Favourite.objects.get(id=new_favorite.id).delete()

        response = self.client.post(
            "/books/favourite/",
            data={
                "book": new_favorite.book.id,
                "user": new_favorite.user.id,
            },
            format='json',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(new_favorite.book.id, response.data['book'])
        self.assertEqual(new_favorite.user.id, response.data['user'])

        # check that there are now two items in the books list
        response = self.client.get("/books/favourite/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEquals(2, len(response.data))

    def test_cannot_create_non_unique_favourite_item(self):
        """Test that a user can create a new favourite item."""
        new_book = BookFactory()
        new_favorite = FavouriteFactory(book=new_book, user=self.user)
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/books/favourite/",
            data={
                "book": new_favorite.book.id,
                "user": new_favorite.user.id,
            },
            format='json',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_deleting_favourite_item(self):
        """Test that a user can delete a favorite item."""
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            "/books/favourite/{}/".format(self.favourite.id),
            format='json',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        # Retrieve the book list check that the list has no items
        response = self.client.get("/books/favourite/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEquals(0, len(response.data))

    def test_another_user_cannot_view_or_delete_favorite_item(self):
        """Test that another user cannot read or delete favourite item."""
        another_user = UserFactory()
        new_book = BookFactory()
        another_favourite = FavouriteFactory(book=new_book, user=self.user)
        self.client.force_authenticate(user=another_user)

        # Retrieve list of todos
        response = self.client.get("/books/favourite/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        # List should be empty since the reading list previously created does not belong to this user
        self.assertEquals(0, len(response.data))

        response = self.client.post(
            "/books/favourite/",
            data={
                "book": another_favourite.book.id,
                "user": another_favourite.user.id,
            },
            format='json',
        )

        # Should not be allowed to POST
        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Should not be allowed to DELETE
        response = self.client.delete(
            "/books/favourite/{}/".format(another_favourite.id),
            format='json',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
