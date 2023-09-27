from django import template


register = template.Library()

bad_words = {
   'bad',
   'hell',
   'Bad',
   'Hell',

}


@register.filter()
def censor(value):
   list = value.split()
   for word in range(len(list)):
      if list[word] in bad_words:
         list[word] = '****'

   return ' '.join(map(str, list))















