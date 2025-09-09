from django import forms
from events.models import EventModel, ParticipantModel, CategoryModel



class StyledFormMixin:
    """ Mixing to apply style to form field"""
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()


    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                print("Inside Date")
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                print("Inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })
    
                
 
# class EventForm(forms.Form):
#     title = forms.CharField(max_length=100, label="Event Name")
#     description = forms.CharField(widget = forms.Textarea,  label ="Event Description")
#     location = forms.CharField(max_length=100)
#     date = forms.DateInput()
#     time = forms.TimeInput()
#     assigned_to = forms.MultipleChoiceField(widget= forms.CheckboxSelectMultiple, choices=[])

#     def __init__(self, *args, **kwargs):
#         # print(args, kwargs)
#         participants = kwargs.pop("participants", [])
#         super().__init__(*args, **kwargs)
#         self.fields['assigned_to'].choices = [
#             (par.id, par.name) for par in participants]
    
               
# Model form

class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = EventModel
        fields = ['title', 'date', 'time', 'location',  'description' ]
        
        widgets = {
            'date': forms.SelectDateWidget(),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            # 'assigned_to': forms.CheckboxSelectMultiple,
        }

    """ Widget using mixins """

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
            
    
class categoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CategoryModel   
        fields = ['name', 'description'] 
        
        

    """ Widget using mixins """

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
        
class participentModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ParticipantModel
        fields = ['name', 'email']
    
        """ Widget using mixins """

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
    
    