from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase

from ...api.serializers import PostListSerializer
from ...api.serializers import PostSerializer
from ...models import Post
from ..factory import PostFactory


class PostApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        post1 = PostFactory()
        post2 = PostFactory(name="Бокс 2")

        url = reverse("post-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Post.objects.filter(pk__in=[post1.pk, post2.pk])
        serializer_data = PostListSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        payload = {"name": "Бокс 1"}

        url = reverse("post-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Post.objects.get(name=payload["name"]))

    def test_get(self):
        post = PostFactory()

        url = reverse("post-detail", kwargs={"pk": post.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = PostSerializer(post).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        post = PostFactory()
        payload = {"name": "Бокс 2"}

        url = reverse("post-detail", kwargs={"pk": post.pk})
        response = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        post_result = Post.objects.get(pk=post.pk)
        self.assertEqual(post_result.name, payload["name"])

    def test_delete(self):
        post = PostFactory()

        url = reverse("post-detail", kwargs={"pk": post.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(pk=post.pk)
