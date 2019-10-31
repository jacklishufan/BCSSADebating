import django_tables2 as tables
from .models import Speaker,User

class SpeakerTable(tables.Table):
  #  average = tables.Column(accessor='get_avg')

    # def render_average(self,record):
    #     return str(record.get_avg)
    #
    # def order_clothing(self, queryset, is_descending):
    #     queryset = queryset.annotate(
    #         amount=tables.F("shirts") + tables.F("pants")
    #     ).order_by(("-" if is_descending else ") + "amount")
    #     return (queryset, True)

    class Meta:
        model = Speaker
        template_name = "django_tables2/bootstrap.html"
        fields = ("name","avg")

class UserTablePublic(tables.Table):
    ballot_set = tables.ManyToManyColumn()
    class Meta:

        model = User
        template_name = "django_tables2/bootstrap.html"
        fields = ("id","name",'time')

class UserTable(tables.Table):
    link = tables.LinkColumn('delete_user',text="DELETE",kwargs={"userid":tables.A("id")})
    ballot_set = tables.ManyToManyColumn()
    class Meta:

        model = User
        template_name = "django_tables2/bootstrap.html"
        fields = ("id","name",'link','time')


# class SpeakerTable(tables.Table):
#         name = tables.Column()
#
# class PersonTable(tables.Table):
#     link = tables.LinkColumn('PaperDisplayDetails', kwargs={"paper_id": A("id")},
#     class Meta:
#         model = Person
#         template_name = 'django_tables2/bootstrap.html'
#        fields = ('id', 'name', )

class FinalSpeakerTable(tables.Table):
  #  average = tables.Column(accessor='get_avg')

    # def render_average(self,record):
    #     return str(record.get_avg)
    #
    # def order_clothing(self, queryset, is_descending):
    #     queryset = queryset.annotate(
    #         amount=tables.F("shirts") + tables.F("pants")
    #     ).order_by(("-" if is_descending else ") + "amount")
    #     return (queryset, True)

    class Meta:
        model = Speaker
        attrs = {"text-aligned": "center"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("name","votes")
