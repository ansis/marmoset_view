#!/usr/bin/env python
"""
marmoset_view.py
"""

import argparse
import getpass

import mechanize
import BeautifulSoup


if (__name__ == '__main__'):

    parser = argparse.ArgumentParser(description='Check Marmoset test results')
    parser.add_argument('course', help='course code (cs246)')
    parser.add_argument('assignment', help='assignment identifier (a1p5e)')
    parser.add_argument('--user', default=getpass.getuser())
    args = parser.parse_args()

    password = getpass.getpass()

    br = mechanize.Browser()

    ## CAS login
    br.open("https://marmoset.student.cs.uwaterloo.ca/")
    br.select_form(nr=0)
    br['username'] = args.user
    br['password'] = password
    br.submit()

    ## Marmoset auth
    br.select_form('PerformLogin')
    br.submit()

    ## Navigate to course
    for link in br.links():
        if args.course in link.text.lower():
            page = br.follow_link(link).read()


    def wantedRow(tag):
        c = tag.get('class')
        if c and c.startswith('r') and len(c) == 2:
            return True

    ## Navigate to assignment page
    soup = BeautifulSoup.BeautifulSoup(page)
    for row in soup.findAll(wantedRow):
        cols = row.findAll('td')
        if cols[0].text.lower().startswith(args.assignment):
            page = br.open(cols[1].find('a').get('href')).read()

    ## Parse results
    soup = BeautifulSoup.BeautifulSoup(page)
    for row in soup.findAll(wantedRow):
        cols = row.findAll('td')
        print "%s     %s" % (cols[1].text, cols[2].text)
