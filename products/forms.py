from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["fullname", "headline", "content", "rating"]
        widgets = {
            "fullname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your Full Name"}
            ),
            "headline": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "What’s most important to know",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "What did you like or dislike? What did you use this product for?",
                }
            ),
        }

