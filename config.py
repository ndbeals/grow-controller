import confuse
import confuse.templates

# raw_settings = confuse.Configuration("GrowController")
# raw_settings.set_file("./config.yaml")


# template = {
#     "dht_pin": confuse.templates.Integer()
# }

# settings = raw_settings.get(template)




# source = confuse.YamlSource('config.yaml')
# config = confuse.RootView([source])
raw_settings = confuse.Configuration("GrowController")
raw_settings.set_file("./config.yaml")
template = {
    'inputs': confuse.Sequence({
        'device': str,
        'name': str,
        'pin': confuse.Integer(),
        # 'pin': confuse.REQUIRED,
        'data': confuse.Optional(str),
        # 'pins': confuse.OneOf([confuse.Sequence(confuse.Integer()),confuse.StrSeq()]),
        'poll_interval': confuse.Optional(float,default=1),
        'channels': confuse.Sequence(confuse.MappingValues(object)),
    }),
    'inps': confuse.Sequence({
        'device': confuse.MappingTemplate({
            # 'device': str,
            'name': str,
            'pin': confuse.Integer(),
        })
    }),
    'triggers': confuse.Sequence({
        'name': str,
        'code': str
    }),
    # 'outputs': confuse.Sequence({
    #     'device': str,
    #     'name': str,
    #     'pin': confuse.Integer(),
    #     # 'pin': confuse.REQUIRED,
    #     # 'data': confuse.Optional(str),
    #     'data': confuse.MappingValues(object),
    #     # 'pins': confuse.OneOf([confuse.Sequence(confuse.Integer()),confuse.StrSeq()]),
    # }),
    # 'outputs': confuse.Sequence({
    #     'device': str,
    #     'name': str,
    #     'pin': confuse.Integer()}
    # ),
    'outputs': confuse.Sequence(confuse.MappingValues(object)),
}

# valid_config = config.get(template)
settings = raw_settings.get(template)
# print("done confiug")


# import pprint
# import yaml

# def ready():
#     with open("test.yaml","r") as fp:
#         d = yaml.load(fp)
#         pprint.pprint(d)

#         return d
# ,
#     'inps': confuse.Sequence({
#         'device': confuse.MappingTemplate({
#             'a': str,
#             'b': str,
#             'c': 0,
#             'd': 10
#         })
#     }),
#     "t": confuse.Sequence({
#         "a": str,
#         "b": str,
#         "c": str
#     }),
#     "tt": confuse.Sequence({
#         "a": str,
#         # "b": str,
#     })