from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class JobQueueManager:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.executor = ThreadPoolExecutor(max_workers=num_threads)
        self.lock = threading.Lock()
        self.jobs = []

    def add_job(self, func, *args, **kwargs):
        with self.lock:
            future = self.executor.submit(func, *args, **kwargs)
            self.jobs.append(future)

    def wait_for_completion(self):
        with self.lock:
            for future in as_completed(self.jobs):
                try:
                    result = future.result()
                    print(f"Job completed with result: {result}")
                except Exception as e:
                    print(f"Job resulted in an exception: {e}")
            self.jobs = []

    def shutdown(self):
        self.executor.shutdown(wait=True)

# Example usage
if __name__ == "__main__":
    import time

    def example_job(duration, value):
        time.sleep(duration)
        return value

    job_manager = JobQueueManager(num_threads=8)

    # Add 20 jobs
    for i in range(20):
        job_manager.add_job(example_job, duration=1, value=i)

    # Wait for all jobs to complete
    job_manager.wait_for_completion()

    # Shutdown the job manager
    job_manager.shutdown()
