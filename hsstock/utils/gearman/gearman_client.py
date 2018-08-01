
import python3_gearman

def check_request_status(job_request):
    if job_request.complete:
        print("Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result))
    elif job_request.timed_out:
        print("Job %s timed out!" % job_request.unique)
    elif job_request.state == 'JOB_UNKNOWN':
        print("Job %s connection failed!" % job_request.unique)

gm_client = python3_gearman.GearmanClient(['10.240.154.201:4730'])

for i in range(1, 10000000):
    completed_job_request = gm_client.submit_job('crawl', "{\"url\":\"http://bim.netease.com\"}", wait_until_complete=False)
    #print(completed_job_request)
    check_request_status(completed_job_request)