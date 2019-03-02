
from memory_profiler import profile

import json

@profile
def main():
    from xml.etree import ElementTree




    string = "<MPD xmlns=\"urn:mpeg:dash:schema:mpd:2011\" minBufferTime=\"PT1.500S\" type=\"static\" mediaPresentationDuration=\"PT0H0M5.834S\" maxSegmentDuration=\"PT0H0M2.000S\" profiles=\"urn:mpeg:dash:profile:isoff-on-demand:2011,http://dashif.org/guidelines/dash264\"><Period duration=\"PT0H0M5.834S\"><AdaptationSet segmentAlignment=\"true\" maxWidth=\"640\" maxHeight=\"590\" maxFrameRate=\"30\" par=\"408960:727040\" lang=\"und\" subsegmentAlignment=\"true\" subsegmentStartsWithSAP=\"1\"><Representation id=\"17964081208230476vd\" mimeType=\"video/mp4\" codecs=\"avc1.4D401F\" width=\"640\" height=\"1136\" frameRate=\"30\" sar=\"639:640\" startWithSAP=\"1\" bandwidth=\"2446944\" FBQualityClass=\"sd\" FBQualityLabel=\"640w\"><BaseURL>https://scontent-mxp1-1.cdninstagram.com/vp/75e4dd3bba7c4c191e065ae2d401b33b/5C7D8070/t50.12441-16/53672166_296458104369852_6468667781471372965_n.mp4?_nc_ht=scontent-mxp1-1.cdninstagram.com</BaseURL><SegmentBase indexRangeExact=\"true\" indexRange=\"930-997\" FBFirstSegmentRange=\"998-753241\" FBSecondSegmentRange=\"753242-1381807\"><Initialization range=\"0-929\"/></SegmentBase></Representation><Representation id=\"17997610147196593v\" mimeType=\"video/mp4\" codecs=\"avc1.4D401F\" width=\"332\" height=\"590\" frameRate=\"30\" sar=\"2655:2656\" startWithSAP=\"1\" bandwidth=\"873855\" FBQualityClass=\"sd\" FBQualityLabel=\"332w\"><BaseURL>https://scontent-mxp1-1.cdninstagram.com/vp/e3b14067ff9adf3636d4593790720294/5C7DB45C/t50.12441-16/53363571_2168351236810915_7591912468076788620_n.mp4?_nc_ht=scontent-mxp1-1.cdninstagram.com</BaseURL><SegmentBase indexRangeExact=\"true\" indexRange=\"931-998\" FBFirstSegmentRange=\"999-265624\" FBSecondSegmentRange=\"265625-500252\"><Initialization range=\"0-930\"/></SegmentBase></Representation></AdaptationSet></Period></MPD>"



    def get_mdp_url(manifest):
        root = ElementTree.fromstring(manifest)
        return root[0][0][0][0].text
        # for child in root:
        #     print(child.tag)
        #     if child.tag == 'Representation':
        #         for grandchild in child:
        #             if grandchild.tag == 'BaseURL':
        #                 return grandchild.text

    print(get_mdp_url(string))



main()
