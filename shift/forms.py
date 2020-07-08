from django import forms
from .models import Schedule,Shop_config,Shop_config_day


class BS4ScheduleForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Schedule
        fields = ('start_time', 'end_time')
        widgets = {

            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if end_time <= start_time:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後にしてください'
            )
        return end_time


class SimpleScheduleForm(forms.ModelForm):
    """シンプルなスケジュール登録用フォーム"""

    class Meta:
        model = Schedule
        fields = ('start_time', 'end_time', 'date')
        widgets = {
            # 'summary': forms.TextInput(attrs={
                # 'class': 'form-control',
            # }),
            'date': forms.HiddenInput,
            'shop':forms.HiddenInput,
        }
class MasterForm(forms.ModelForm):
    """シンプルなスケジュール登録用フォーム"""

    class Meta:
        model = Schedule
        fields = ('start_at', 'end_at', 'date')
        widgets = {
            # 'summary': forms.TextInput(attrs={
                # 'class': 'form-control',
            # }),
            'date': forms.HiddenInput,
            'shop':forms.HiddenInput,
        }
class Shop_base_configForm(forms.ModelForm):
    class Meta:
        model = Shop_config
        fields=('shops','base_pa_a','base_pa_b','base_pa_c',)
        wifgets={
                'shops':forms.HiddenInput,}

class Shop_config_dayForm(forms.ModelForm):
    class Meta:
        model = Shop_config_day
        fields=('day_need','date')
        wifgets={'date': forms.HiddenInput,
                'shops':forms.HiddenInput,}