from django import forms
from .models import Post, BlockList


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            print(field)
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Post
        exclude = ("user", )


class BlockListForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BlockListForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            print(field)
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = BlockList
        exclude = ("user", )