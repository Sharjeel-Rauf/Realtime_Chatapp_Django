from django import forms

class VideoURLForm(forms.Form):
    video_url = forms.URLField(label="YouTube Video URL", required=True)