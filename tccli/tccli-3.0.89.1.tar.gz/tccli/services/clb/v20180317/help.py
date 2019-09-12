# -*- coding: utf-8 -*-
DESC = "clb-2018-03-17"
INFO = {
  "RegisterTargets": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ListenerId",
        "desc": "负载均衡监听器 ID"
      },
      {
        "name": "Targets",
        "desc": "待绑定的后端服务列表，数组长度最大支持20"
      },
      {
        "name": "LocationId",
        "desc": "转发规则的ID，当绑定后端服务到七层转发规则时，必须提供此参数或Domain+Url两者之一"
      },
      {
        "name": "Domain",
        "desc": "目标转发规则的域名，提供LocationId参数时本参数不生效"
      },
      {
        "name": "Url",
        "desc": "目标转发规则的URL，提供LocationId参数时本参数不生效"
      }
    ],
    "desc": "RegisterTargets 接口用来将一台或多台后端服务绑定到负载均衡的监听器（或7层转发规则），在此之前您需要先行创建相关的4层监听器或7层转发规则。对于四层监听器（TCP、UDP），只需指定监听器ID即可，对于七层监听器（HTTP、HTTPS），还需通过LocationId或者Domain+Url指定转发规则。\n本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。"
  },
  "SetLoadBalancerSecurityGroups": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "SecurityGroups",
        "desc": "安全组ID构成的数组，一个负载均衡实例最多可绑定50个安全组，如果要解绑所有安全组，可不传此参数，或传入空数组。"
      }
    ],
    "desc": "SetLoadBalancerSecurityGroups 接口支持对一个公网负载均衡实例执行设置（绑定、解绑）安全组操作。查询一个负载均衡实例目前已绑定的安全组，可使用 DescribeLoadBalancers 接口。本接口是set语义，\n绑定操作时，入参需要传入负载均衡实例要绑定的所有安全组（已绑定的+新增绑定的）。\n解绑操作时，入参需要传入负载均衡实例执行解绑后所绑定的所有安全组；如果要解绑所有安全组，可不传此参数，或传入空数组。注意：内网负载均衡不支持绑定安全组。"
  },
  "DescribeClassicalLBListeners": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ListenerIds",
        "desc": "负载均衡监听器ID列表"
      },
      {
        "name": "Protocol",
        "desc": "负载均衡监听的协议, 'TCP', 'UDP', 'HTTP', 'HTTPS'"
      },
      {
        "name": "ListenerPort",
        "desc": "负载均衡监听端口， 范围[1-65535]"
      },
      {
        "name": "Status",
        "desc": "监听器的状态，0 表示创建中，1 表示运行中"
      }
    ],
    "desc": "DescribeClassicalLBListeners 接口用于获取传统型负载均衡的监听器信息。"
  },
  "DeleteListener": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ListenerId",
        "desc": "要删除的监听器 ID"
      }
    ],
    "desc": "本接口用来删除负载均衡实例下的监听器（四层和七层）。\n本接口为异步接口，接口返回成功后，需以得到的 RequestID 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。"
  },
  "SetSecurityGroupForLoadbalancers": {
    "params": [
      {
        "name": "SecurityGroup",
        "desc": "安全组ID，如 sg-12345678"
      },
      {
        "name": "OperationType",
        "desc": "ADD 绑定安全组；\nDEL 解绑安全组"
      },
      {
        "name": "LoadBalancerIds",
        "desc": "负载均衡实例ID数组"
      }
    ],
    "desc": "绑定或解绑一个安全组到多个公网负载均衡实例。注意：内网负载均衡不支持绑定安全组。"
  },
  "ReplaceCertForLoadBalancers": {
    "params": [
      {
        "name": "OldCertificateId",
        "desc": "需要被替换的证书的ID，可以是服务端证书或客户端证书"
      },
      {
        "name": "Certificate",
        "desc": "新证书的内容等相关信息"
      }
    ],
    "desc": "ReplaceCertForLoadBalancers 接口用以替换负载均衡实例所关联的证书，对于各个地域的负载均衡，如果指定的老的证书ID与其有关联关系，则会先解除关联，再建立新证书与该负载均衡的关联关系。\n此接口支持替换服务端证书或客户端证书。\n需要使用的新证书，可以通过传入证书ID来指定，如果不指定证书ID，则必须传入证书内容等相关信息，用以新建证书并绑定至负载均衡。\n注：本接口仅可从广州地域调用，其他地域存在域名解析问题，会报错。"
  },
  "CreateRule": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ListenerId",
        "desc": "监听器 ID"
      },
      {
        "name": "Rules",
        "desc": "新建转发规则的信息"
      }
    ],
    "desc": "CreateRule 接口用于在一个已存在的负载均衡七层监听器下创建转发规则，七层监听器中，后端服务必须绑定到规则上而非监听器上。\n本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。"
  },
  "AutoRewrite": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例ID"
      },
      {
        "name": "ListenerId",
        "desc": "HTTPS:443监听器的ID"
      },
      {
        "name": "Domains",
        "desc": "HTTPS:443监听器下需要重定向的域名"
      }
    ],
    "desc": "用户需要先创建出一个HTTPS:443监听器，并在其下创建转发规则。通过调用本接口，系统会自动创建出一个HTTP:80监听器（如果之前不存在），并在其下创建转发规则，与HTTPS:443监听器下的Domains（在入参中指定）对应。创建成功后可以通过HTTP:80地址自动跳转为HTTPS:443地址进行访问。"
  },
  "ModifyDomain": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ListenerId",
        "desc": "负载均衡监听器 ID"
      },
      {
        "name": "Domain",
        "desc": "监听器下的某个旧域名。"
      },
      {
        "name": "NewDomain",
        "desc": "新域名，\t长度限制为：1-120。有三种使用格式：非正则表达式格式，通配符格式，正则表达式格式。非正则表达式格式只能使用字母、数字、‘-’、‘.’。通配符格式的使用 ‘*’ 只能在开头或者结尾。正则表达式以'~'开头。"
      }
    ],
    "desc": "ModifyDomain接口用来修改负载均衡七层监听器下的域名。\n本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。"
  },
  "DescribeClassicalLBTargets": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      }
    ],
    "desc": "DescribeClassicalLBTargets用于获取传统型负载均衡绑定的后端服务"
  },
  "DeregisterTargetsFromClassicalLB": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "InstanceIds",
        "desc": "后端服务的实例ID列表"
      }
    ],
    "desc": "DeregisterTargetsFromClassicalLB 接口用于解绑负载均衡后端服务。\n本接口为异步接口，接口返回成功后，需以返回的 RequestId 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。"
  },
  "DescribeClassicalLBHealthStatus": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ListenerId",
        "desc": "负载均衡监听器ID"
      }
    ],
    "desc": "DescribeClassicalLBHealthStatus用于获取传统型负载均衡后端的健康状态"
  },
  "ModifyListener": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ListenerId",
        "desc": "负载均衡监听器 ID"
      },
      {
        "name": "ListenerName",
        "desc": "新的监听器名称"
      },
      {
        "name": "SessionExpireTime",
        "desc": "会话保持时间，单位：秒。可选值：30~3600，默认 0，表示不开启。此参数仅适用于TCP/UDP监听器。"
      },
      {
        "name": "HealthCheck",
        "desc": "健康检查相关参数，此参数仅适用于TCP/UDP/TCP_SSL监听器"
      },
      {
        "name": "Certificate",
        "desc": "证书相关信息，此参数仅适用于HTTPS/TCP_SSL监听器"
      },
      {
        "name": "Scheduler",
        "desc": "监听器转发的方式。可选值：WRR、LEAST_CONN\n分别表示按权重轮询、最小连接数， 默认为 WRR。"
      }
    ],
    "desc": "ModifyListener接口用来修改负载均衡监听器的属性，包括监听器名称、健康检查参数、证书信息、转发策略等。本接口不支持传统型负载均衡。\n本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。"
  },
  "DeleteLoadBalancer": {
    "params": [
      {
        "name": "LoadBalancerIds",
        "desc": "要删除的负载均衡实例 ID数组，数组大小最大支持20"
      }
    ],
    "desc": "DeleteLoadBalancer 接口用以删除指定的一个或多个负载均衡实例。\n本接口为异步接口，接口返回成功后，需以返回的 RequestId 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。"
  },
  "DeleteRule": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ListenerId",
        "desc": "负载均衡监听器 ID"
      },
      {
        "name": "LocationIds",
        "desc": "要删除的转发规则的ID组成的数组"
      },
      {
        "name": "Domain",
        "desc": "要删除的转发规则的域名，已提供LocationIds参数时本参数不生效"
      },
      {
        "name": "Url",
        "desc": "要删除的转发规则的转发路径，已提供LocationIds参数时本参数不生效"
      }
    ],
    "desc": "DeleteRule 接口用来删除负载均衡实例七层监听器下的转发规则。\n本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。"
  },
  "DescribeLoadBalancers": {
    "params": [
      {
        "name": "LoadBalancerIds",
        "desc": "负载均衡实例 ID。"
      },
      {
        "name": "LoadBalancerType",
        "desc": "负载均衡实例的网络类型：\nOPEN：公网属性， INTERNAL：内网属性。"
      },
      {
        "name": "Forward",
        "desc": "负载均衡实例的类型。1：通用的负载均衡实例，0：传统型负载均衡实例"
      },
      {
        "name": "LoadBalancerName",
        "desc": "负载均衡实例的名称。"
      },
      {
        "name": "Domain",
        "desc": "腾讯云为负载均衡实例分配的域名，本参数仅对传统型公网负载均衡才有意义。"
      },
      {
        "name": "LoadBalancerVips",
        "desc": "负载均衡实例的 VIP 地址，支持多个。"
      },
      {
        "name": "BackendPublicIps",
        "desc": "负载均衡绑定的后端服务的外网 IP。"
      },
      {
        "name": "BackendPrivateIps",
        "desc": "负载均衡绑定的后端服务的内网 IP。"
      },
      {
        "name": "Offset",
        "desc": "数据偏移量，默认为 0。"
      },
      {
        "name": "Limit",
        "desc": "返回负载均衡实例的个数，默认为 20。"
      },
      {
        "name": "OrderBy",
        "desc": "排序参数，支持以下字段：LoadBalancerName，CreateTime，Domain，LoadBalancerType。"
      },
      {
        "name": "OrderType",
        "desc": "1：倒序，0：顺序，默认按照创建时间倒序。"
      },
      {
        "name": "SearchKey",
        "desc": "搜索字段，模糊匹配名称、域名、VIP。"
      },
      {
        "name": "ProjectId",
        "desc": "负载均衡实例所属的项目 ID，可以通过 DescribeProject 接口获取。"
      },
      {
        "name": "WithRs",
        "desc": "负载均衡是否绑定后端服务，0：没有绑定后端服务，1：绑定后端服务，-1：查询全部。"
      },
      {
        "name": "VpcId",
        "desc": "负载均衡实例所属私有网络，如 vpc-bhqkbhdx，\n基础网络不支持通过VpcId查询。"
      },
      {
        "name": "SecurityGroup",
        "desc": "安全组ID，如 sg-m1cc9123"
      },
      {
        "name": "MasterZone",
        "desc": "主可用区ID，如 ：\"100001\" （对应的是广州一区）"
      }
    ],
    "desc": "查询负载均衡实例列表\n"
  },
  "DescribeListeners": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ListenerIds",
        "desc": "要查询的负载均衡监听器 ID数组"
      },
      {
        "name": "Protocol",
        "desc": "要查询的监听器协议类型，取值 TCP | UDP | HTTP | HTTPS | TCP_SSL"
      },
      {
        "name": "Port",
        "desc": "要查询的监听器的端口"
      }
    ],
    "desc": "DescribeListeners 接口可根据负载均衡器 ID，监听器的协议或端口作为过滤条件获取监听器列表。如果不指定任何过滤条件，默认返该负载均衡器下的默认数据长度（20 个）的监听器。"
  },
  "CreateListener": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "Ports",
        "desc": "要将监听器创建到哪些端口，每个端口对应一个新的监听器"
      },
      {
        "name": "Protocol",
        "desc": "监听器协议： TCP | UDP | HTTP | HTTPS | TCP_SSL（TCP_SSL 正在内测中，如需使用请通过工单申请）"
      },
      {
        "name": "ListenerNames",
        "desc": "要创建的监听器名称列表，名称与Ports数组按序一一对应，如不需立即命名，则无需提供此参数"
      },
      {
        "name": "HealthCheck",
        "desc": "健康检查相关参数，此参数仅适用于TCP/UDP/TCP_SSL监听器"
      },
      {
        "name": "Certificate",
        "desc": "证书相关信息，此参数仅适用于HTTPS/TCP_SSL监听器"
      },
      {
        "name": "SessionExpireTime",
        "desc": "会话保持时间，单位：秒。可选值：30~3600，默认 0，表示不开启。此参数仅适用于TCP/UDP监听器。"
      },
      {
        "name": "Scheduler",
        "desc": "监听器转发的方式。可选值：WRR、LEAST_CONN\n分别表示按权重轮询、最小连接数， 默认为 WRR。此参数仅适用于TCP/UDP/TCP_SSL监听器。"
      },
      {
        "name": "SniSwitch",
        "desc": "是否开启SNI特性，此参数仅适用于HTTPS监听器。"
      }
    ],
    "desc": "在一个负载均衡实例下创建监听器。\n本接口为异步接口，接口返回成功后，需以返回的 RequestId 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。"
  },
  "ModifyTargetWeight": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ListenerId",
        "desc": "负载均衡监听器 ID"
      },
      {
        "name": "LocationId",
        "desc": "转发规则的ID，当绑定机器到七层转发规则时，必须提供此参数或Domain+Url两者之一"
      },
      {
        "name": "Domain",
        "desc": "目标规则的域名，提供LocationId参数时本参数不生效"
      },
      {
        "name": "Url",
        "desc": "目标规则的URL，提供LocationId参数时本参数不生效"
      },
      {
        "name": "Targets",
        "desc": "要修改权重的后端服务列表"
      },
      {
        "name": "Weight",
        "desc": "后端服务服务新的转发权重，取值范围：0~100，默认值10。如果设置了 Targets.Weight 参数，则此参数不生效。"
      }
    ],
    "desc": "ModifyTargetWeight 接口用于修改负载均衡绑定的后端服务的转发权重。\n本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。"
  },
  "DescribeTaskStatus": {
    "params": [
      {
        "name": "TaskId",
        "desc": "请求ID，即接口返回的 RequestId 参数"
      }
    ],
    "desc": "本接口用于查询异步任务的执行状态，对于非查询类的接口（创建/删除负载均衡实例、监听器、规则以及绑定或解绑后端服务等），在接口调用成功后，都需要使用本接口查询任务最终是否执行成功。"
  },
  "ModifyRule": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ListenerId",
        "desc": "负载均衡监听器 ID"
      },
      {
        "name": "LocationId",
        "desc": "要修改的转发规则的 ID。"
      },
      {
        "name": "Url",
        "desc": "转发规则的新的转发路径，如不需修改Url，则不需提供此参数"
      },
      {
        "name": "HealthCheck",
        "desc": "健康检查信息"
      },
      {
        "name": "Scheduler",
        "desc": "规则的请求转发方式，可选值：WRR、LEAST_CONN、IP_HASH\n分别表示按权重轮询、最小连接数、按IP哈希， 默认为 WRR。"
      },
      {
        "name": "SessionExpireTime",
        "desc": "会话保持时间"
      },
      {
        "name": "ForwardType",
        "desc": "负载均衡实例与后端服务之间的转发协议，默认HTTP，可取值：HTTP、HTTPS"
      }
    ],
    "desc": "ModifyRule 接口用来修改负载均衡七层监听器下的转发规则的各项属性，包括转发路径、健康检查属性、转发策略等。\n本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。"
  },
  "DescribeTargetHealth": {
    "params": [
      {
        "name": "LoadBalancerIds",
        "desc": "要查询的负载均衡实例 ID列表"
      }
    ],
    "desc": "DescribeTargetHealth 接口用来获取负载均衡后端服务的健康检查结果，不支持传统型负载均衡。"
  },
  "DescribeTargets": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ListenerIds",
        "desc": "监听器 ID列表"
      },
      {
        "name": "Protocol",
        "desc": "监听器协议类型"
      },
      {
        "name": "Port",
        "desc": "监听器端口"
      }
    ],
    "desc": "DescribeTargets 接口用来查询负载均衡实例的某些监听器绑定的后端服务列表。"
  },
  "DescribeRewrite": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例ID"
      },
      {
        "name": "SourceListenerIds",
        "desc": "负载均衡监听器ID数组"
      },
      {
        "name": "SourceLocationIds",
        "desc": "负载均衡转发规则的ID数组"
      }
    ],
    "desc": "DescribeRewrite 接口可根据负载均衡实例ID，查询一个负载均衡实例下转发规则的重定向关系。如果不指定监听器ID或转发规则ID，则返回该负载均衡实例下的所有重定向关系。"
  },
  "RegisterTargetsWithClassicalLB": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "Targets",
        "desc": "后端服务信息"
      }
    ],
    "desc": "RegisterTargetsWithClassicalLB 接口用于绑定后端服务到传统型负载均衡。\n本接口为异步接口，接口返回成功后，需以返回的 RequestId 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。"
  },
  "ModifyTargetPort": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ListenerId",
        "desc": "负载均衡监听器 ID"
      },
      {
        "name": "Targets",
        "desc": "要修改端口的后端服务列表"
      },
      {
        "name": "NewPort",
        "desc": "后端服务绑定到监听器或转发规则的新端口"
      },
      {
        "name": "LocationId",
        "desc": "转发规则的ID，当后端服务绑定到七层转发规则时，必须提供此参数或Domain+Url两者之一"
      },
      {
        "name": "Domain",
        "desc": "目标规则的域名，提供LocationId参数时本参数不生效"
      },
      {
        "name": "Url",
        "desc": "目标规则的URL，提供LocationId参数时本参数不生效"
      }
    ],
    "desc": "ModifyTargetPort接口用于修改监听器绑定的后端服务的端口。\n本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。"
  },
  "DeregisterTargets": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID，格式如 lb-12345678"
      },
      {
        "name": "ListenerId",
        "desc": "监听器 ID，格式如 lbl-12345678"
      },
      {
        "name": "Targets",
        "desc": "要解绑的后端服务列表，数组长度最大支持20"
      },
      {
        "name": "LocationId",
        "desc": "转发规则的ID，格式如 loc-12345678，当从七层转发规则解绑机器时，必须提供此参数或Domain+Url两者之一"
      },
      {
        "name": "Domain",
        "desc": "目标规则的域名，提供LocationId参数时本参数不生效"
      },
      {
        "name": "Url",
        "desc": "目标规则的URL，提供LocationId参数时本参数不生效"
      }
    ],
    "desc": "DeregisterTargets 接口用来将一台或多台后端服务从负载均衡的监听器或转发规则上解绑，对于四层监听器，只需指定监听器ID即可，对于七层监听器，还需通过LocationId或Domain+Url指定转发规则。\n本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。"
  },
  "ModifyLoadBalancerAttributes": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡的唯一ID"
      },
      {
        "name": "LoadBalancerName",
        "desc": "负载均衡实例名称"
      },
      {
        "name": "TargetRegionInfo",
        "desc": "负载均衡绑定的后端服务的地域信息"
      }
    ],
    "desc": "修改负载均衡实例的属性。支持修改负载均衡实例的名称、设置负载均衡的跨域属性。"
  },
  "DescribeClassicalLBByInstanceId": {
    "params": [
      {
        "name": "InstanceIds",
        "desc": "后端实例ID列表"
      }
    ],
    "desc": "DescribeClassicalLBByInstanceId用于通过后端实例ID获取传统型负载均衡ID列表"
  },
  "BatchModifyTargetWeight": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例 ID"
      },
      {
        "name": "ModifyList",
        "desc": "要批量修改权重的列表"
      }
    ],
    "desc": "BatchModifyTargetWeight接口用于批量修改负载均衡监听器绑定的后端机器的转发权重，暂时只支持HTTP/HTTPS监听器。不支持传统型负载均衡。\n本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。"
  },
  "DeleteRewrite": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例ID"
      },
      {
        "name": "SourceListenerId",
        "desc": "源监听器ID"
      },
      {
        "name": "TargetListenerId",
        "desc": "目标监听器ID"
      },
      {
        "name": "RewriteInfos",
        "desc": "转发规则之间的重定向关系"
      }
    ],
    "desc": "DeleteRewrite 接口支持删除指定转发规则之间的重定向关系。"
  },
  "CreateLoadBalancer": {
    "params": [
      {
        "name": "LoadBalancerType",
        "desc": "负载均衡实例的网络类型：\nOPEN：公网属性， INTERNAL：内网属性。"
      },
      {
        "name": "Forward",
        "desc": "负载均衡实例的类型。1：通用的负载均衡实例，目前只支持传入1"
      },
      {
        "name": "LoadBalancerName",
        "desc": "负载均衡实例的名称，只在创建一个实例的时候才会生效。规则：1-50 个英文、汉字、数字、连接线“-”或下划线“_”。\n注意：如果名称与系统中已有负载均衡实例的名称相同，则系统将会自动生成此次创建的负载均衡实例的名称。"
      },
      {
        "name": "VpcId",
        "desc": "负载均衡后端目标设备所属的网络 ID，可以通过 DescribeVpcEx 接口获取。 不传此参数则默认为基础网络（\"0\"）。"
      },
      {
        "name": "SubnetId",
        "desc": "在私有网络内购买内网负载均衡实例的情况下，必须指定子网 ID，内网负载均衡实例的 VIP 将从这个子网中产生。其它情况不支持该参数。"
      },
      {
        "name": "ProjectId",
        "desc": "负载均衡实例所属的项目 ID，可以通过 DescribeProject 接口获取。不传此参数则视为默认项目。"
      },
      {
        "name": "AddressIPVersion",
        "desc": "仅适用于公网负载均衡。IP版本，IPV4 | IPV6，默认值 IPV4。"
      },
      {
        "name": "Number",
        "desc": "创建负载均衡的个数，默认值 1。"
      },
      {
        "name": "MasterZoneId",
        "desc": "仅适用于公网负载均衡。设置跨可用区容灾时的主可用区ID，例如 100001 或 ap-guangzhou-1\n注：主可用区是需要承载流量的可用区，备可用区默认不承载流量，主可用区不可用时才使用备可用区，平台将为您自动选择最佳备可用区。可通过 DescribeMasterZones 接口查询一个地域的主可用区的列表。"
      },
      {
        "name": "ZoneId",
        "desc": "仅适用于公网负载均衡。可用区ID，指定可用区以创建负载均衡实例。如：ap-guangzhou-1"
      },
      {
        "name": "AnycastZone",
        "desc": "仅适用于公网负载均衡。Anycast的发布域，可取 ZONE_A 或 ZONE_B。仅带宽非上移用户支持此参数。"
      },
      {
        "name": "InternetAccessible",
        "desc": "仅适用于公网负载均衡。负载均衡的网络计费方式，此参数仅对带宽上移用户生效。"
      },
      {
        "name": "Tags",
        "desc": "购买负载均衡同时，给负载均衡打上标签"
      }
    ],
    "desc": "CreateLoadBalancer 接口用来创建负载均衡实例。为了使用负载均衡服务，您必须购买一个或多个负载均衡实例。成功调用该接口后，会返回负载均衡实例的唯一 ID。负载均衡实例的类型分为：公网、内网。详情可参考产品说明中的产品类型。\n注意：(1)指定可用区申请负载均衡、跨zone容灾【如需使用，请提交工单（ https://console.cloud.tencent.com/workorder/category ）申请】；(2)目前只有北京、上海、广州支持IPv6；\n本接口为异步接口，接口成功返回后，可使用 DescribeLoadBalancers 接口查询负载均衡实例的状态（如创建中、正常），以确定是否创建成功。"
  },
  "ManualRewrite": {
    "params": [
      {
        "name": "LoadBalancerId",
        "desc": "负载均衡实例ID"
      },
      {
        "name": "SourceListenerId",
        "desc": "源监听器ID"
      },
      {
        "name": "TargetListenerId",
        "desc": "目标监听器ID"
      },
      {
        "name": "RewriteInfos",
        "desc": "转发规则之间的重定向关系"
      }
    ],
    "desc": "用户手动配置原访问地址和重定向地址，系统自动将原访问地址的请求重定向至对应路径的目的地址。同一域名下可以配置多条路径作为重定向策略，实现http/https之间请求的自动跳转。设置重定向时，需满足如下约束条件：若A已经重定向至B，则A不能再重定向至C（除非先删除老的重定向关系，再建立新的重定向关系），B不能重定向至任何其它地址。"
  }
}