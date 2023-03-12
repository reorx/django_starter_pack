import params
from params.contrib.django import use_params_class_view

from ..contact.models import Contact
from ..contact import api as contact_api
from ..utils.models_formatter import make_model_formatter, make_model_encoder
from ..utils.models_paginator import PaginatorParams, paginate_queryset
from ..lib.views import JSONView
#from ..schemas.contact import validate_contact_schema


class Status:
    success = 'success'
    error = 'error'


def make_resp_data(data, status=Status.success):
    d = {
        'status': status,
        'data': data,
    }
    return d


format_contact = make_model_formatter([
    'id',
    'email',
    'company',
    'note',
    'created_at',
    'updated_at',
])

contact_encoder = make_model_encoder(Contact, format_contact)


class ContactsListView(JSONView):
    @use_params_class_view(PaginatorParams)
    def get(self, request):
        args = request.params

        qs = contact_api.get_list()
        paged = paginate_queryset(qs, args.page, args.limit, args.sort, args.order),

        return self.json_response(make_resp_data(paged), encoder=contact_encoder)


class ContactsInfoView(JSONView):
    @use_params_class_view({
        'id': params.IntegerField(required=True),
    })

    def get(self, request):
        c = contact_api.get(id=request.params.id)
        return self.json_response(make_resp_data(c), encoder=contact_encoder)


#class ContactsCreateView(JSONView):
#    def post(self, request):
#        data = validate_contact_schema(self.json)
#        c = Contact(**data)
#        contact_api.create(c)
#        return self.json_response(make_resp_data(c), encoder=contact_encoder)
