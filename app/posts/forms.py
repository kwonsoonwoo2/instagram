from django import forms

from .models import Post


class PostCreateForm(forms.Form):
    photo = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file',
            }
        )
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    def save(self, **kwargs):
        post = Post.objects.create(
            photo=self.cleaned_data['photo'],
            **kwargs,
        )

        comment_content = self.cleaned_data.get('comment')
        if comment_content:
            # Comment.objects.create(
            #     post=post,
            #     author=post.author,
            #     content=comment_content,
            # )
            post.comment_contents.create(
                author=post.author,
                content=comment_content,
            )
        return post
