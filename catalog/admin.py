from django.contrib import admin
from .models import Book, Genre, Author, Languange, BookInstance
# Register your models here.
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    
    def get_extra(self, request, obj=None, **kwargs):
        extra = 2
        if obj:
            return extra - obj.bookinstance_set.count()
        return extra
    
class BookInline(admin.TabularInline):
    model = Book
    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','date_of_birth','date_of_death')
    fields = [('first_name','last_name'),('date_of_birth','date_of_death')]
    inlines = [BookInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre','languange')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter=('due_back','status','book')
    list_display = ('status','browwer','due_back','id','book')
    
    fieldsets = (
        (
            None, {
                'fields':('book','imprint','id')
            }
            ),
        (
            'Availability',{
                'fields':[('status','due_back','browwer')]
            }
        )
    )
    
admin.site.register(Author,AuthorAdmin)

#admin.site.register(Book)
admin.site.register(Genre)
#admin.site.register(Author)
admin.site.register(Languange)
#admin.site.register(BookInstance)