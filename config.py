__FILETYPES = {
    "010": "file",
    "014": "socket",
    "012": "link",
    "060": "block dev",
    "004": "dir",
    "020": "char dev",
    "0O1": "FIFO"
               }

__SPECIALBITS = {
    "0": "None",
    "512": "STICKYBIT",
    "1024": "SETGID",
    "1536": "SETGID/STICKYBIT",
    "2048": "SETUID",
    "2560": "SETUID/STICKYBIT",
    "3072": "SETUID/SETGID",
    "3584": "SETUID/SETGID/STICKYBIT"
}

__WHITELIST = []

__DT_LOOKUP = {
    0: 'CLEAN',
    1: 'DANGEROUS_FILE',
    2: 'DANGEROUS_URL',
    3: 'DANGEROUS_CONTENT',
    4: 'MAYBE_DANGEROUS_CONTENT',
    5: 'UNCOMMON_CONTENT',
    6: 'USER_VALIDATED',
    7: 'DANGEROUS_HOST',
    8: 'POTENTIALLY_UNWANTED',
    9: 'MAX'
}

__ARTIFACTS_LIST = "artifacts.json"
