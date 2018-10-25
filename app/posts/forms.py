from django import forms

from .models import Post, Comment


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


class CommentCreateForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 2,
            }
        )
    )

    def save(self, post, **kwargs):
        content = self.cleaned_data['content']
        return post.comments.create(
            content=content,
            **kwargs,
        )



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2,
                }
            )
        }