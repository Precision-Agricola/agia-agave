#%%
import backblaze
from dataclasses import dataclass
from wasabi import Printer
msg = Printer()

@dataclass
class BucketCredentials:
	account: str
	app_key: str
	bucket_name: str
	model_path: str


class ModelsSync:
	def __init__(self, bucket):
		self.client = backblaze.Blocking(
			key_id=bucket.account,
			key=bucket.app_key,
		)
		self.client.authorize()
		self.model = self.download_model(bucket)
		self.client.close()
	
	def download_model(self, bucket):
		model = self.client.download_by_name(
			bucket_name=bucket.bucket_name,
			file_name=bucket.model_path
			)
		return model

def main():
	msg.divider("Enter your account id and app key")
	account_id = input("Enter your account id: ")
	app_key = input("Enter your app key: ")
	bucket_name = "AgiaDev"
	model_path = "models/agave_2023-01-11.zip"
	bucket_credentials = BucketCredentials(account_id, app_key, bucket_name, model_path)
	model = ModelsSync(bucket_credentials).model
	msg.good("Model downloaded")
	return model

if __name__ == "__main__":
	model = main()
