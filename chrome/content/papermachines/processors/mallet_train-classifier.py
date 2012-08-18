#!/usr/bin/env python
import sys, os, logging, traceback, time, subprocess
import mallet

class MalletClassifier(mallet.MalletLDA):
	"""
	Train a classifier
	"""
	def _basic_params(self):
		self.template_name = "mallet-classifier"

	def process(self):
		self.dry_run = False
		self.name = "mallet_train-classifier"

		self._setup_mallet_instances(False)

		self.mallet_output = os.path.join(self.mallet_out_dir, "trained.classifier")
		process_args = self.mallet + ["cc.mallet.classify.tui.Vectors2Classify",
			"--input", self.instance_file,
			"--output-classifier", self.mallet_output,
			"--trainer", "MaxEnt",
			"--noOverwriteProgressMessages", "true"]

		logging.info("begin training classifier")

		start_time = time.time()
		if not self.dry_run:
			classifier_return = subprocess.call(process_args, stdout=self.progress_file, stderr=self.progress_file)

		finished = "Classifier trained in " + str(time.time() - start_time) + " seconds"
		logging.info(finished)

		params = {'DONE': finished}

		self.write_html(params)

if __name__ == "__main__":
	try:
		logging.basicConfig(filename=os.path.join(sys.argv[3], "logs", "mallet_train-classifier.log"), level=logging.INFO)
		processor = MalletClassifier(sys.argv, track_progress=True)
		processor.process()
	except:
		logging.error(traceback.format_exc())