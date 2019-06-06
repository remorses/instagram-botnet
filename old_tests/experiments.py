from xml.etree import ElementTree
import ffmpeg
import os
from random import random

string = """<MPD xmlns=\"urn:mpeg:dash:schema:mpd:2011\" minBufferTime=\"PT1.500S\" type=\"static\" mediaPresentationDuration=\"PT0H1M0.070S\" maxSegmentDuration=\"PT0H0M2.020S\" profiles=\"urn:mpeg:dash:profile:isoff-on-demand:2011,http://dashif.org/
guidelines/dash264\"><Period duration=\"PT0H1M0.070S\"><AdaptationSet segmentAlignment=\"true\" lang=\"und\" subsegmentAlignment=\"true\" subsegmentStartsWithSAP=\"1\"><Representation id=\"17998003366084790ad\" mimeType=\"audio/mp4\" codecs=\"mp4
a.40.2\" audioSamplingRate=\"44100\" startWithSAP=\"1\" bandwidth=\"65964\"><AudioChannelConfiguration schemeIdUri=\"urn:mpeg:dash:23003:3:audio_channel_configuration:2011\" value=\"2\"/><BaseURL>https://scontent-mxp1-1.cdninstagram.com/vp/f9f288
a81a93d67053a34ec8d8c70689/5C7DE945/t50.2886-16/49335811_275270176479795_4112980307395428073_n.mp4?_nc_ht=scontent-mxp1-1.cdninstagram.com</BaseURL><SegmentBase indexRangeExact=\"true\" indexRange=\"840-1243\" FBFirstSegmentRange=\"1244-18490\" F
BSecondSegmentRange=\"18491-34962\"><Initialization range=\"0-839\"/></SegmentBase></Representation></AdaptationSet><AdaptationSet segmentAlignment=\"true\" maxWidth=\"720\" maxHeight=\"900\" maxFrameRate=\"30\" par=\"452:566\" lang=\"und\" subse
gmentAlignment=\"true\" subsegmentStartsWithSAP=\"1\"><Representation id=\"17847729046332851vd\" mimeType=\"video/mp4\" codecs=\"avc1.4D401F\" width=\"452\" height=\"566\" frameRate=\"30\" sar=\"1:1\" startWithSAP=\"1\" bandwidth=\"221953\" FBQua
lityClass=\"sd\" FBQualityLabel=\"452w\"><BaseURL>https://scontent-mxp1-1.cdninstagram.com/vp/8bc67ec8cfe6daf1cd6f47d7ea688f30/5C7E3168/t50.2886-16/50431121_594924300920837_38858319701395766_n.mp4?_nc_ht=scontent-mxp1-1.cdninstagram.com</BaseURL>
<SegmentBase indexRangeExact=\"true\" indexRange=\"910-1301\" FBFirstSegmentRange=\"1302-23553\" FBSecondSegmentRange=\"23554-59460\"><Initialization range=\"0-909\"/></SegmentBase></Representation><Representation id=\"18006495649097946v\" mimeTy
pe=\"video/mp4\" codecs=\"avc1.4D401F\" width=\"284\" height=\"356\" frameRate=\"30\" sar=\"1:1\" startWithSAP=\"1\" bandwidth=\"112707\" FBQualityClass=\"sd\" FBQualityLabel=\"284w\"><BaseURL>https://scontent-mxp1-1.cdninstagram.com/vp/6d5a33c79
169ebc4398c9eca11f552a2/5C7E6F63/t50.2886-16/50259299_231394417748483_5290620231680510418_n.mp4?_nc_ht=scontent-mxp1-1.cdninstagram.com</BaseURL><SegmentBase indexRangeExact=\"true\" indexRange=\"910-1301\" FBFirstSegmentRange=\"1302-13206\" FBSe
condSegmentRange=\"13207-32728\"><Initialization range=\"0-909\"/></SegmentBase></Representation><Representation id=\"17996949475093919v\" mimeType=\"video/mp4\" codecs=\"avc1.4D401F\" width=\"720\" height=\"900\" frameRate=\"30\" sar=\"1:1\" sta
rtWithSAP=\"1\" bandwidth=\"459623\" FBQualityClass=\"hd\" FBQualityLabel=\"720w\"><BaseURL>https://scontent-mxp1-1.cdninstagram.com/vp/1e8900385bef06481f7018388dc98238/5C7E2222/t50.2886-16/50317307_124640905243240_921695025927607707_n.mp4?_nc_ht
=scontent-mxp1-1.cdninstagram.com</BaseURL><SegmentBase indexRangeExact=\"true\" indexRange=\"910-1301\" FBFirstSegmentRange=\"1302-57502\" FBSecondSegmentRange=\"57503-129877\"><Initialization range=\"0-909\"/></SegmentBase></Representation></Ad
aptationSet></Period></MPD>"""

class temporary_write:
        def __init__(self,  data, path=str(random())[3:]):
                self.path = path
                self.data = data
                f = open(self.path, 'a+b')
                f.write(self.data)
                f.close()

        __enter__ = lambda self: self.path
        __exit__ = lambda self, a, b, c: os.remove(self.path)


manifest = string.replace('\n','')

with temporary_write(manifest, path='manifest.mpd') as path:

    (ffmpeg
        .input(manifest, format='dash')
        .output('out.mp4')
        .run()
    )


root = ElementTree.fromstring(manifest)
for a in root.findall('.//{urn:mpeg:dash:schema:mpd:2011}BaseURL'):
    print (a.attrib)
