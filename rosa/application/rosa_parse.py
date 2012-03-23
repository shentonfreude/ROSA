#!/usr/bin/env python
# 2007-12-18 Chris Shenton
# ROSA requires authentication by form.
# While it rewrites URLs by suffixing ";jsessionid=..."
# we have to set a cookie to get the XML file.
#
# ROSA XML doesn't use attributes on tags except for the top-level <rosa/>
# Next level in is <application/> and its tags for each app
# (NOT wrapped in an <applications> tag).
#
# 2012-03-23 My password no longer works and I cannot script RSA auth.
# After manual RSA auth, grab from
# https://merope.hq.nasa.gov/rosa/ws/hdmsrosa/all/main/RosaExportXml
# It's 21MB at present.
# xml.parsers.expat.ExpatError: not well-formed (invalid token): line 334227, column 69
# Due to embedded ^K ?
from elementtree import ElementTree as ET
import urllib
import httplib2


class Rosa(object):
    def __init__(self):
        self.http_port = 443
        self.http_host = 'merope.hq.nasa.gov'
        self.http_login_url  = 'https://%s/rosa/ws' % self.http_host
        self.http_xml_path = '/rosa/ws/hdmsrosa/all/main/RosaExportXml'
        self.http_xml_url  = 'https://%s%s' % (self.http_host,self.http_xml_path)
        self.http_cookie = None
        self.TOO_MANY_VALUES = 30       # 24 different status_of_app, sheesh
        self.DIRTY_FILE_PATH = '/tmp/rosa-dirty.xml' # before BASIS crap removed
        self.CLEAN_FILE_PATH = '/tmp/rosa-clean.xml' # after  BASIS crap removed

    def _uniq(self, things):
        return sorted(tuple(set(things)))
    
    def _values(self, things):
        """Show choices if not too many things, else just 'text' generic.
        """
        if len(things) < 1:
            return "{text}"
        if len(things) > self.TOO_MANY_VALUES:
            return "{ text }"
        return "{ %s }" % " | ".join(['"%s"' % e for e in things])

    def http_login(self, user='cshenton', password='chsh2474'):
        """POST credentials to the app and save the cookie for subsequent requests.
        """
        body = urllib.urlencode({'user': user, 'password': password})
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        http = httplib2.Http()
        response, content = http.request(self.http_login_url, 'POST', headers=headers, body=body)
        self.http_cookie = response['set-cookie']
        if not self.http_cookie:
            raise Exception, 'Could not get valid cookie from login:', e
        
    def http_get_xml(self):
        """Get the XML body, need to pass it the cookie we got from login.
        TODO: what is the content type?
        """
        if not self.http_cookie:
            self.http_login()           #?? need a way to pass creds
        headers = {'Cookie': self.http_cookie}
        http = httplib2.Http()
        response, content = http.request(self.http_xml_url, 'GET', headers=headers)
        print "http response=%s" % response
        self.xml_text = content
        
    def file_get_xml(self, filename='rosaExportXML.xml'):
        """Read the XML from the given filename, save as .xml_text for parsing.
        """
        self.xml_text = file(filename).read().replace(chr(11), '') # ^K noise

    def parse_xml(self):
        self.xml = ET.fromstring(self.xml_text)

    def show_some_apps(self, max_apps=2):
        napps = 0
        for app in self.xml.getiterator('application'):
            napps += 1
            if napps > max_apps:
                raise SystemExit, "Ending after %d elements" % max_apps
            #import pdb; pdb.set_trace()
            text = app.text
            text = text and len(text) > 40 and text[:40] + "..." or text
            print "tag=%s text=%s" % (app.tag, text)
            appdata = app.getchildren()
            for elem in appdata:
                print "\t%s = %s" % (elem.tag, elem.text)
                # some of these have subelements, crazy ones.
        
    def get_application_tags(self):
        """Tally all the tags across all applications, there's strange stuff.
        """
        tags = self.xml.findall("./application/*") # doesn't get subelements?
        tag_names = [t.tag for t in tags]
        tag_names = [n for n in tag_names if not self.is_ignorable_tag(n)]
        return self._uniq(tag_names)

        
    def get_application_values(self):
        """Taly all tags' values across all apps, in order to find unique vals for schemas.
        This is woefully inefficient but will get 'er done.
        """
        tag_names = self.get_application_tags()
        for tn in tag_names:
            tag_instances = self.xml.findall("./application/%s" % tn)
            # Can't strip, some have text=None
            vals = self._uniq([s.text for s in tag_instances])
            if len(vals) > self.TOO_MANY_VALUES:
                print "%s: TOO MANY: %s" % (tn, len(vals))
            else:
                print "%s: %s" % (tn, vals)
            kids = self.xml.findall("./application/%s/*" % tn)
            if kids:
                kids_tags = self._uniq([k.tag for k in kids])
                print "%s : KIDS TAGS=%s" % (" "*len(tn), kids_tags)
                for kt in kids_tags:
                    kid_vals = self.xml.findall("./application/%s/%s" % (tn,kt))
                    kid_vals = self._uniq([k.text for k in kid_vals])
                    if len(kid_vals) > self.TOO_MANY_VALUES:
                        print "%s :       VAL=%s" % (" "*len(tn), "TOO MAN=%s" % len(kid_vals))
                    else:
                        for v in kid_vals:
                            print "%s :       VAL=%s" % (" "*len(tn), v)
                
    def get_schema_rnc(self):
        """Produce a schema based on the app tags.
        Where we've got a reasonable number of values, make them choices.
        Else we'll guess at text.
        This is a horrible clone of get_application_values;
        Should do it generically with recursion, then
        walk some results to filter differently.
        How to spec vocab? maybe: element ename { xsd:string {pattern="\w{,10}"}}
        How do we indicate we can have many choices? e.g., lang=python,java ?
        TODO: allow empty outer tags for sw_lang thing
        TODO: urlencode crap in the text tags
        TODO: make optional '*' some tag content, oish.
        TODO: why doesn't it like <application> in the second instance? 
        """
        tag_names = self.get_application_tags()
        tag_first = True
        print "element rosa {"
        print "   attribute rosa-version {text},"
        print "   attribute produced_date {text},"
        print "   element application {"
        for tn in tag_names:
            tag_instances = self.xml.findall("./application/%s" % tn)
            # Can't strip, some have text=None
            vals = self._uniq([s.text for s in tag_instances])
            vals = [v.strip() for v in vals if v]
            kids = self.xml.findall("./application/%s/*" % tn)
            if tag_first:
                tag_first = False
            else:
                print "      &"
            if not kids:                # if we have kids we ignore any text in this tag, WRONG?
                print "      element %s %s" % (tn, self._values(vals))
            else:
                print "      element %s {" % tn
                kids_tags = self._uniq([k.tag for k in kids])
                for kt in kids_tags:
                    kid_vals = self.xml.findall("./application/%s/%s" % (tn,kt))
                    kid_vals = self._uniq([k.text for k in kid_vals])
                    print "         element %s %s" % (kt, self._values(kid_vals))
                print "}"
        print "   }"
        print "}"
                

    def remove_basis_crap(self):
        """Walk the apps and remove nodes matching basis noise tags.
        I anticipate this being used to preprocess the ROSA XML,
        save result XML to file, then validate that so schema doesn't
        have to know about basis nonsense. Why doesn't ROSA remove this?
        """
        for app in self.xml.getiterator('application'):
            for child in app.getchildren():
                if self.is_ignorable_tag(child.tag):
                    app.remove(child)
            
    def is_ignorable_tag(self, tagname):
        """Return True if tag is junk and should be ignored; I had to lowercase these. 
        Sandra Schmidt says these fields are "Basis DMS Fields" and 
          All of the fields ending in "_All" are the string version of
          a like-named field which is defined as a compound/array field.
        """
        dms_tags = (
            'accessed',
            'access_history',
            'cm_entered_date',
            'cm_submitter',
            'combined_search',
            'doclevel',
            'doclevelcomment',
            'doc_number',
            'entered_by',
            'entered_date',
            'fileext',
            'filename',
            'file_size',
            'fk_doc_number',
            'group',
            'group_code',
            'group_read',
            'html_object_link',
            'hw_support_all',
            'icon',
            'mimetype',
            're_entered_by',
            're_entered_date',
            'requests',
            'syskey',
            'text',
            'userid',
            'userlevel',
            'version_doc_key',
            'version_highest_version_flag',
            'version_highest_version_key',
            'version_version_number',
            )
        return (tagname in dms_tags) or (tagname.endswith('_all'))
            

def main():
    r = Rosa()
    r.file_get_xml('/Users/cshenton/Documents/rosaExportXml.xml')
    #r.http_get_xml()
    print r.xml_text[:1000]

    r.parse_xml()

    #dirty = ET.ElementTree(r.xml)
    #dirty.write(r.DIRTY_FILE_PATH)
    r.remove_basis_crap()
    #clean = ET.ElementTree(r.xml)       # I hope this is different now
    #clean.write(r.CLEAN_FILE_PATH)

    r.show_some_apps()
    #r.get_application_values()
    #r.get_schema_rnc()


if __name__ == '__main__':
    main()
