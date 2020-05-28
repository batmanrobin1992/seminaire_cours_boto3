# Le code suivant vient de la documentation de Boto3. 
# Il est utilisait pour principe de test de fonctionnalité de l'environnement de travail.
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html
import boto3

sqs = boto3.resource('sqs')


class SQS:

    def __init__(self, queue_name, message_body, message_attribute_names):
        self.queue_name = queue_name
        self.message_body = message_body
        self.message_attribute_names = message_attribute_names

    def sending_message(self):
        queue: sqs.Queue = sqs.get_queue_by_name(QueueName=self.queue_name)
        # Create a new message
        queue.send_message(MessageBody=self.message_body)

    def processing_message(self):
        queue: sqs.Queue = sqs.get_queue_by_name(QueueName=self.queue_name)

        # Process messages by printing out body and optional author name
        for message in queue.receive_messages(MessageAttributeNames=[self.message_attribute_names]):
            # Get the custom author message attribute if it was set
            author_text = ''
            if message.message_attributes is not None:
                author_name = message.message_attributes.get('Author').get('StringValue')
                if author_name:
                    author_text = ' ({0})'.format(author_name)

            # Print out the body and author (if set)
            print('Hello, {0}!{1}'.format(message.body, author_text))

            # Let the queue know that the message is processed
            message.delete()


if __name__ == "__main__":
    sqs_test = SQS('test', 'world', 'Author')
    sqs_test.sending_message()
    sqs_test.processing_message()
