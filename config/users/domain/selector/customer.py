from ...models import Customer




class CustomerSelector:


    @staticmethod
    def get_or_create(*, email: str):
        customer, created = Customer.objects.get_or_create()
        return customer, created