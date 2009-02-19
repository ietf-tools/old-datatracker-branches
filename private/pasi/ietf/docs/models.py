# Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved. Contact: Pasi Eronen <pasi.eronen@nokia.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
#  * Neither the name of the Nokia Corporation and/or its
#    subsidiary(-ies) nor the names of its contributors may be used
#    to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from django.db import models

class RfcEditorQueue(models.Model):
    draft = models.CharField(maxlength=200,primary_key=True)
    date_received = models.DateField()
    state = models.CharField(maxlength=200, blank=True, null=True)
    # currently, queue2.xml does not have this information, so
    # this field will be NULL (but we could get it from other sources)
    state_date = models.DateField(blank=True,null=True)
    def __str__(self):
        return "RfcEditorQueue"+str([self.draft, self.date_received, self.state])
    class Meta:
        db_table = "rfc_editor_queue_mirror"
    class Admin:
        pass
  
class RfcIndex(models.Model):
    rfc_number = models.IntegerField(primary_key=True)
    title = models.CharField(maxlength=250)
    authors = models.CharField(maxlength=250)
    rfc_published_date = models.DateField()
    current_status = models.CharField(maxlength=50,null=True)
    updates = models.CharField(maxlength=200,blank=True,null=True)
    updated_by = models.CharField(maxlength=200,blank=True,null=True)
    obsoletes = models.CharField(maxlength=200,blank=True,null=True)
    obsoleted_by = models.CharField(maxlength=200,blank=True,null=True)
    also = models.CharField(maxlength=50,blank=True,null=True)
    draft = models.CharField(maxlength=200,null=True)
    has_errata = models.BooleanField()
    def __str__(self):
        return "RfcIndex"+str(self.rfc_number)
    class Meta:
        db_table = "rfc_index_mirror"
    class Admin:
        pass

class DraftVersions(models.Model):
    # Django does not support multi-column primary keys, so
    # we can't use filename+revision. But the key for this table
    # does not really matter, so we'll have an 'id' field
    id = models.AutoField(primary_key=True)
    filename = models.CharField(maxlength=200)
    revision = models.CharField(maxlength=2)
    revision_date = models.DateField()
    def __str__(self):
        return "DraftVersions"+filename+revision+str(revision_date)
    class Meta:
        db_table = "draft_versions_mirror"
    class Admin:
        pass
    
