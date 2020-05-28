from src.python.test_boto3.test import SQS


def main():

    sqs_test = SQS('test', 'world', 'Author')
    sqs_test.sending_message()
    sqs_test.processing_message()


if __name__ == "__main__":
    main()
