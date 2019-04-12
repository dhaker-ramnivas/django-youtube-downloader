
###setup
>
1) have to install redis for queue
2) install celery for backgound process

3) check redis-cli is working or not
4) run celery for background process 
    command :  celery -A django_server worker --loglevel=info



#APIS
##1) check status of task
   method : POST
   {
    "task_id": "celery_task_id" #pass celery task id 
   }
   
 ##2) stop long running task
   method : POST
   {
    "task_id": "celery_task_id" #pass celery task id 
   }
   
 ##3) request for a new youtube video
  method : GET
   pass youtube video id and task will run in background and immediate responce will return to user
   
   
   
   
   
   
 # TASK 2
 
 >
 There is a file named RandomSongs.py which play some random song from path /media/music
 
 COMMAND *python3 manage.py RandomSongs.py"
 
 
 
 
 