# coding: utf-8

from os.path import join, dirname, abspath

from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory, APIClient
from model_mommy import mommy

from albums import views


factory = APIRequestFactory()
client = APIClient()
IMG_PATH = join(dirname(abspath(__file__)), 'img/')


class TestAlbumListView(TestCase):

    def setUp(self):
        self.album = mommy.make('albums.Album', title='White Album')
        self.view = views.AlbumListAPIView.as_view()
        self.url = reverse('album-list')

        request = factory.get('/')
        self.response = self.view(request).render()

    def test_view_url(self):
        url = self.url
        response = client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_albums_list_view_should_return_200(self):
        response = self.response
        self.assertEqual(response.status_code, 200)

    def test_should_return_a_list_of_albums(self):
        response = self.response
        album = self.album

        self.assertEquals(type(response.data), list)

        self.assertEquals(response.data[0]['title'], album.title)

    def test_create_album(self):
        data = {
            'band': self.album.band.pk, 'title': 'abbey road',
            'date_released': '2013-11-30',
            'cover': open(join(IMG_PATH, 'mock-img.jpeg')),
        }
        request = factory.post('/', data=data)
        response = self.view(request).render()
        self.assertEqual(response.status_code, 201)
        self.assertIn('covers/mock-img', response.data['cover'])


class TestAlbumDetailView(TestCase):

    def setUp(self):
        self.album = mommy.make('albums.Album', title='White Album')
        self.view = views.AlbumRetrieveAPIView.as_view()
        self.url = reverse('album-detail', kwargs={'pk': self.album.pk})

        request = factory.get('/')
        self.response = self.view(request, pk=self.album.pk).render()

    def test_should_return_200(self):
        response = self.response
        self.assertEqual(response.status_code, 200)

    def test_view_url(self):
        url = self.url
        response = client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_update_album(self):
        data = {
            'band': self.album.band.pk, 'title': 'Revolver',
            'date_released': '1970-11-30',
            'cover': open(join(IMG_PATH, 'mock-img.jpeg')),
        }
        request = factory.put('/', data=data)
        response = self.view(request, pk=1).render()
        self.assertEqual(response.status_code, 200)


class TestAlbumTracksView(TestCase):

    def setUp(self):
        self.album = mommy.make('albums.Album', title='White Album')
        self.tracks = mommy.make('tracks.Track', album=self.album, _quantity=5)
        self.view = views.AlbumTracksAPIView.as_view()
        self.url = reverse('album-track-list', kwargs={'pk': self.album.pk})

        request = factory.get('/')
        self.response = self.view(request, pk=self.album.pk).render()

    def test_should_return_200(self):
        response = self.response
        self.assertEqual(response.status_code, 200)

    def test_view_url(self):
        url = self.url
        response = client.get(url)

        self.assertEqual(response.status_code, 200)


class TestAlbumCommentListView(TestCase):
    def setUp(self):
        self.album = mommy.make('albums.Album')
        self.view = views.AlbumCommentListAPIView.as_view()

    def test_endpoint_should_only_list_comments_from_album_pk(self):
        mommy.make_recipe('comments.album_comment', object_id=self.album.pk)
        mommy.make_recipe('comments.album_comment')

        request = factory.get('/')
        response = self.view(request, pk=self.album.pk).render()
        self.assertEqual(len(response.data), 1)
