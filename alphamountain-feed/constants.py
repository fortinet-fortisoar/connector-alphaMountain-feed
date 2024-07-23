"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

API_VERSION = '1'
REQUEST_TYPE = 'partner.info'

DEFAULT_CATEGORIES = {"0": "Unrated", "1": "Abortion", "10": "Chat/IM/SMS", "11": "Child Pornography/Abuse",
                      "12": "Content Servers", "13": "Dating/Personals", "14": "Digital Postcards",
                      "15": "Drugs/Controlled Substances", "16": "Education", "17": "Email", "18": "Entertainment",
                      "19": "Extreme/Gruesome", "2": "Ads/Analytics", "20": "File Sharing/Storage", "21": "Finance",
                      "22": "For Kids", "23": "Forums", "24": "Gambling", "25": "Games", "26": "Government/Legal",
                      "27": "Hacking", "28": "Hate/Discrimination", "29": "Health", "3": "Adult/Mature",
                      "30": "Hobbies/Recreation", "31": "Hosting", "32": "Humor/Comics", "33": "Alternative Ideology",
                      "34": "Information Technology", "35": "Information/Computer Security", "36": "Infrastructure/IOT",
                      "37": "Job Search", "38": "Lingerie/Swimsuit", "39": "Malicious", "4": "Alcohol",
                      "40": "Marijuana", "41": "Marketing/Merchandising", "42": "Media Sharing", "43": "Military",
                      "44": "Mixed Content/Potentially Adult", "45": "News", "46": "Non-Profit/Advocacy",
                      "47": "Nudity", "48": "Parked Site", "49": "Peer-to-Peer (P2P)", "5": "Arts/Culture",
                      "50": "Personal Sites/Blogs", "51": "Phishing", "52": "Piracy/Plagiarism",
                      "53": "Politics/Opinion", "54": "Pornography", "55": "Potentially Unwanted Programs",
                      "56": "Productivity Applications", "57": "Anonymizers", "58": "Real Estate", "59": "Reference",
                      "6": "Auctions/Classifieds", "60": "Religion", "61": "Remote Access", "62": "Restaurants/Food",
                      "63": "Scam/Illegal/Unethical", "64": "Search Engines/Portals", "65": "Sex Education",
                      "66": "Shopping", "67": "Social Networking", "68": "Society/Lifestyles",
                      "69": "Software Downloads", "7": "Audio", "70": "Spam", "71": "Sports", "72": "Suspicious",
                      "73": "Telephony", "74": "Tobacco", "75": "Translation", "76": "Travel", "77": "URL Redirect",
                      "78": "Vehicles", "79": "Video/Multimedia", "8": "Brokerage/Trading", "80": "Violence",
                      "81": "Virtual Meetings", "82": "Weapons", "83": "AI/ML Applications",
                      "84": "Alternative Currency", "85": "Dynamic DNS", "86": "Login/Verification",
                      "87": "Newly Registered Domains", "88": "Promotional Compensation", "9": "Business/Economy"}

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 ' \
                     '(KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36'
