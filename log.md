#### notes  
* json的库函数，load()和dump()是处理文件数据的，相应的我猜loads和dumps应该就是其他的。（十有八九是错的）

* BASE_DIR is where your manage.py lies, and PROJECT_ROOT is BASE_DIR + your_project_name (where settings.py is).

* HOW TO USE BASE_DIR?
> from django.conf import settings # correct way
> base_dir = settings.BASE_DIR    

* 判断list中是否有某个值
  `if xxx in listone  `