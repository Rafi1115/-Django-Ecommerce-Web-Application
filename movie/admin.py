from django.contrib import admin

from .models import (OurUser, Person, Movie, Celebrite,
                      Role, Crew, Vote, TvMovie, ComingSoon, TvName )

admin.site.register(OurUser)
admin.site.register(Person)
admin.site.register(Celebrite)
admin.site.register(TvName)
admin.site.register(Role)
admin.site.register(Crew)
admin.site.register(Vote)
admin.site.register(TvMovie)
admin.site.register(ComingSoon)




class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_plot',)
    prepopulated_fields = {'slug': ('title',)} # new

admin.site.register(Movie, MovieAdmin)