import python3_gearman

gm_worker = python3_gearman.GearmanWorker(['10.240.154.201:4730'])


def task_listener_reverse(gearman_worker, gearman_job):
    print('Reversing string: ' + gearman_job.data)
    return gearman_job.data[::-1]


# gm_worker.set_client_id is optional
gm_worker.set_client_id('python-worker3')
gm_worker.register_task('crawl', task_listener_reverse)

# Enter our work loop and call gm_worker.after_poll() after each time we timeout/see socket activity
gm_worker.work()
