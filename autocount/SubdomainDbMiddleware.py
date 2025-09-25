# from django.db import connections
# from django.conf import settings
# from django.utils.deprecation import MiddlewareMixin
#
#
# class SubdomainDatabaseMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # Get the subdomain from the request
#         host = request.get_host()
#         subdomain = host.split('.')[0]  # Extract subdomain
#
#         # Map subdomain to a database name or configuration
#         db_name = self.get_db_for_subdomain(subdomain)
#
#         # If a valid subdomain, change the database settings
#         if db_name:
#             # Update the DATABASES setting dynamically
#             settings.DATABASES['default'] = {
#                 'ENGINE': 'django.db.backends.postgresql',
#                 'NAME': db_name,
#                 'USER': 'your_db_user',
#                 'PASSWORD': 'your_db_password',
#                 'HOST': 'your_db_host',
#                 'PORT': 'your_db_port',
#             }
#
#             # Ensure the connection uses the right database
#             connections['default'].close()
#             connections['default'].connect()
#
#     def get_db_for_subdomain(self, subdomain):
#         # Define your mapping logic between subdomain and DB name
#         db_mapping = {
#             'sub1': 'db_for_sub1',
#             'sub2': 'db_for_sub2',
#             'sub3': 'db_for_sub3',
#             # Add more subdomains and their respective DB names
#         }
#         return db_mapping.get(subdomain)
