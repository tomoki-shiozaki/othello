from django import forms


class GuestGameCreationForm(forms.Form):
    black_player = forms.CharField(
        max_length=255,
        label="黒のプレイヤー",
    )
    white_player = forms.CharField(
        max_length=255,
        label="白のプレイヤー",
    )
