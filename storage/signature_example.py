from signature import CloudStorageURLSigner

private_key = '''-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC+sOkKRMrEBB+a\nQF7S0ME8DDx3k8EqyjOD9reI9BlBOVEZGC5QwtfCNjmjtRqsLbq3a/vTy2FQXNvq\nr9CGyn/Ydd/72rVqHmBZQq3MmZnQ6lY2dtlvjynJyQr4WuqFJ1ULH5qy/87qOnZO\nXSxTQXbLUcpCsCyz/eCagKDHXzj7AwWgzqwp75Janpzdqw784VwL7P4bLqyEInF4\n/hqaDmvBAKJBGXXxyD+3ADxHNcSiRoTSXclgtXlR9wQQx/msAk2qZzXuWg96YryX\nKD0B2H4hOwNfZQ9d/AmYXrDY0FkpdxK7id2wkJJhxzdqkrBnVIvALHWpp0+qt4jT\nw/4oI1AtAgMBAAECggEBAI/rCRbc8IOb8RYD+wz0zMI7Ie/FrgZTcSnprH9Kaz0U\nuyZLX7lINHq5Xis15hmIseD5OKiSWLHEQ54Obz0r2+1MmW2FlWGv51u2vWErlDFe\niw60CErwK8PFXegvBczU8JRil+j8s/eHg/6Ex41WXQf6hMJsIHD/7OHurmmKboDS\na2jMYMM+XP1DBepj3HSMJk7EwD4VPXcpA6nlkUsToUgZVhtMOsoyVOKaM3S6t+ef\nJCwr2dykXSSf+FXiurhuIh2xgf8ZGkoFbfF9DB/IXPSheak+pNv0iPot+VhIy4qa\n2oZLGO+hr9pj40c++vcVM10vjJEkgWoZhEvAHQ+pNGkCgYEA43VcZBET9j4zL3my\nqLlNgzZMYvK9ofh8IrxDuxgJY82Su+78vYvifDrQXstP49eLZU5oWsgR8MrwdVlZ\nhvTC1pI01yXSE2/BQldUkE4dJatlEyFJXKdYdO1O9+pLVwVrG3uK3/Vt9lcvXnin\ng/R1DKXX8Ei6CU6FftWOUwRRMJ8CgYEA1p542L/PN87d9ZDi1/DTUTdett1DHUzV\nwQhOs8PJnL44UeOWuKJIG0KOIoiBSlqBl1i7Men1RNhR0UGGERtMyNxovMABnc6d\na4O6DpSXo8rhYrRXEA8gL5KrK+ncWAeBhUZ9A0kxvvTIvR1XYshlMU9q7DSmALE0\n345fB0dbD7MCgYBklYB+y8KNEOJnqyRjUlZBoOBUnU1Yc97JKYG2GaIFXWH2828W\njuZf005TrQquEaIV8X9aLcEpP0ToT9O0R0Zlxo/RWGs2pyPKJ35AthpTjyCKPh0H\n+QS36D0Uiqo4WDAOHirCcPDoj5Nl7mr9gjvElQ4Rtsd12CBWfy+J7I3OtwKBgQDG\nUFz+fA7wVLkIxr62JxQ9AdsFQmNX2b3Sxuhid9H+gk7sbE7DgUD7334TLuu5VvRU\nc2tWbgdzfCfuIovNltpW6EPn1cwok9kmlewAuRF+CmRFnrqsXi2xh+efhlNTDGyE\nSGQP+zx6ZRpwlYJAB0hqTiZQ6T1TemuO/7GTuj3MvQKBgQDSqIyf1BGuoMW6krvl\nEFyIEHvs3YQIQRiuhJRZV+DRoSR8YJi5uJXpJXjamyPOOPonrsPOgV+M1sR014wU\nvVDEn2JYEckqj7MA+1jKC6IH1yBoB0HE4OpxDFIykQkzxPXmv9WoBsEM4+NznCS9\n2Op5bUbHMDChdyQiRgYcsgdT+A==\n-----END PRIVATE KEY-----\n'''
signer = CloudStorageURLSigner(private_key,
                               'shipshack@shipshack-143320.iam.gserviceaccount.com',
                               'https://storage.googleapis.com')

file_path = '/%s/%s' % ('shipshack-processed', '2014/10/29/1414582666-a0b41080189236beb1d37faefb71d0e5.jpg')

print 'Retrieving file...'
print '=================='
r = signer.get_url(file_path)
print r
