# -*- coding: utf-8 -*-
DESC = "tts-2019-08-23"
INFO = {
  "TextToVoice": {
    "params": [
      {
        "name": "Text",
        "desc": "合成语音的源文本，按UTF-8编码统一计算。\n中文最大支持100个汉字（全角标点符号算一个汉字）；英文最大支持400个字母（半角标点符号算一个字母）。包含空格等字符时需要url encode再传输。"
      },
      {
        "name": "SessionId",
        "desc": "一次请求对应一个SessionId，会原样返回，建议传入类似于uuid的字符串防止重复。"
      },
      {
        "name": "ModelType",
        "desc": "模型类型，1-默认模型。"
      },
      {
        "name": "Volume",
        "desc": "音量大小，范围：[0，10]，分别对应11个等级的音量，默认为0，代表正常音量。没有静音选项。\n输入除以上整数之外的其他参数不生效，按默认值处理。"
      },
      {
        "name": "Speed",
        "desc": "语速，范围：[-2，2]，分别对应不同语速：<li>-2代表0.6倍</li><li>-1代表0.8倍</li><li>0代表1.0倍（默认）</li><li>1代表1.2倍</li><li>2代表1.5倍</li>输入除以上整数之外的其他参数不生效，按默认值处理。"
      },
      {
        "name": "ProjectId",
        "desc": "项目id，用户自定义，默认为0。"
      },
      {
        "name": "VoiceType",
        "desc": "音色<li>0-亲和女声(默认)</li><li>1-亲和男声</li><li>2-成熟男声</li><li>3-活力男声</li><li>4-温暖女声</li><li>5-情感女声</li><li>6-情感男声</li>"
      },
      {
        "name": "PrimaryLanguage",
        "desc": "主语言类型：<li>1-中文（默认）</li><li>2-英文</li>"
      },
      {
        "name": "SampleRate",
        "desc": "音频采样率：<li>16000：16k（默认）</li><li>8000：8k</li>"
      },
      {
        "name": "Codec",
        "desc": "返回音频格式，可取值：wav（默认），mp3"
      }
    ],
    "desc": "腾讯云语音合成技术（TTS）可以将任意文本转化为语音，实现让机器和应用张口说话。\n腾讯TTS技术可以应用到很多场景，比如，移动APP语音播报新闻；智能设备语音提醒；依靠网上现有节目或少量录音，快速合成明星语音，降低邀约成本；支持车载导航语音合成的个性化语音播报。\n内测期间免费使用。"
  }
}