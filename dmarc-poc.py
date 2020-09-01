#!/usr/bin/python

# ****************************************************************************
# Purpose:
# Assist System Administrators in implementing DMARC, SPF, 
# and DKIM by asking questions and creating a file with the 
# information needed to create the related DNS records.
# ****************************************************************************
# Creator:          Tim Lansing
# Creation Date: 1 September 2020 
# ****************************************************************************
# Notes:
# This script was created using:
#     - Python 3.8.2.
# ****************************************************************************
# History:
# 1 September 2020 - Tim Lansing - Initial creation.
# ****************************************************************************

# Declare global variables.
domain_name = ""
subdomain_name = ""
parent_domain_name = ""
dmarc_policy = ""
dmarc_subdomain_policy = ""
dmarc_policies = {
    "m": "none",
    "q": "quarantine",
    "r": "reject"
}
dmarc_failure_reporting_option = ""
dmarc_dkim_alignment = ""
dmarc_spf_alignment = ""
dmarc_aggregate_email_address = ""
dmarc_forensic_email_address = ""

# Main function to be ran.
def main():
    displayWelcomeMessage()
    askQuestions()
    printOutput()

# Display the welcome message.
def displayWelcomeMessage():
    print("")
    print("****************************************************************************")
    print("Welcome. The purpose of this script is to assist in implementing")
    print("DMARC, SPF, and DKIM.")
    print("")
    print("WARNING: This script is currently a proof of concept and a work")
    print("in progress.")
    print(" 1. Confirm the validity of its output.")
    print(" 2. Ensure your input is correct. Input validation needs to be added.")
    print("****************************************************************************")

# Ask questions for the input needed.
def askQuestions():
    # Declare global variables to be used.
    global domain_name
    global dmarc_policy
    global dmarc_subdomain_policy
    global dmarc_failure_reporting_option
    global dmarc_dkim_alignment
    global dmarc_spf_alignment
    global dmarc_aggregate_email_address
    global dmarc_forensic_email_address

    # Get the domain name.
    print("")
    domain_name = input("Domain name: ")
    setSubdomain()

    # Get the DMARC policy.
    dmarc_policy = ""
    while "" == dmarc_policy:
        print("")
        print("Do you want to monitor, quarantine, or reject emails to your domain")
        print("that do not pass SPF and do not pass DKIM?")
        print("")
        print("Monitor- Recommended when first configuring DMARC.")
        print("Quarantine- Recommended be used before setting to reject. Emails")
        print("    should go to the SPAM / Junk mail folder if they do not pass.")
        print("Reject- Preferred because malicious emails may not arrive to the user.")
        print("    However, legitimate emails not passing may also be dropped. This")
        print("    is also recommended for domains that do not send email.")
        print("Enter:")
        print("'m' for monitor")
        print("'q' for quarantine")
        print("'r' for reject")
        user_input = ""
        user_input = input("Policy selection: ")
        dmarc_policy = dmarc_policies.get(user_input, "")
        if ("" == dmarc_policy):
            print("")
            print("Sorry, that is not a valid choice.")

    # Get subdomain policy, if wanted.
    user_input = ""
    while "y" != user_input and "n" != user_input:
        print("")
        print("Do you want a different setting for subdomains under this domain?")
        print("Enter: 'y' for yes or 'n' for no.")
        user_input = input("Selection: ")
        if ("y" != user_input and "n" != user_input):
            print("")
            print("Sorry, that is not a valid choice.")
    if ("y" == user_input):
        while "" == dmarc_subdomain_policy:
            print("")
            print("Enter:")
            print("'m' for monitor")
            print("'q' for quarantine")
            print("'r' for reject")
            user_input = ""
            user_input = input("Policy selection: ")
            dmarc_subdomain_policy = dmarc_policies.get(user_input, "")
            if ("" == dmarc_subdomain_policy):
                print("")
                print("Sorry, that is not a valid choice.")

    # Get DKIM and SPF alignment settings.
    user_input = ""
    while "y" != user_input and "n" != user_input:
        print("")
        print("Will the email server used always exactly match the domain '"+domain_name+"'?")
        if ("" == parent_domain_name):
            print("Consider if the server for '"+domain_name+"'")
            print("    will be used to send emails for any subdomains.")
        else:
            print("Consider if emails for '"+domain_name+"'")
            print("will be sent by the server for '"+parent_domain_name+"'.")
            print("Or, if its own server will send emails for any subdomains under it.")
        print("If so, then answer 'no'.")
        print("WARNING: If unsure we recomend answering 'no'. Answering 'yes' will")
        print("    increase security, but it may cause legitimate emails to be dropped")
        print("    if not configured correctly.")
        print("Enter: 'y' for yes or 'n' for no.")
        user_input = input("Selection: ")
        if ("y" != user_input and "n" != user_input):
            print("")
            print("Sorry, that is not a valid choice.")
    if ("y" == user_input):
        dmarc_dkim_alignment = "; adkim=s"
        dmarc_spf_alignment = "; aspf=s"

    # Get aggregate reporting email address if reports are wanted.
    user_input = ""
    while "y" != user_input and "n" != user_input:
        print("")
        print("Would you like to receive aggregate reports? We recommend to do so.")
        print("WARNING: Email addresses are public. It is recommended to use")
        print("    dedicated email addresses and deploy abuse countermeasures.")
        print("WARNING: If emails are going to a domain other than the one being")
        print("    configured then a DNS entry will need to be made on that domain as")
        print("    well. If it goes to a DMARC services provider then they will likely take")
        print("    care of this for you. Consult with them to be sure.")
        print("Enter: 'y' for yes or 'n' for no.")
        user_input = input("Selection: ")
        if ("y" != user_input and "n" != user_input):
            print("")
            print("Sorry, that is not a valid choice.")
    if ("y" == user_input):
        dmarc_aggregate_email_address = input("Aggregate email address: ")

    # Get forensic reporting email address and reporting option if reports are wanted.
    user_input = ""
    while "y" != user_input and "n" != user_input:
        print("")
        print("Would you like to receive forensic reports?")
        print("Recommended for troubleshooting or if policy is set to quarantine or reject.")
        print("WARNING: Email addresses are public. It is recommended to use")
        print("    dedicated email addresses and deploy abuse countermeasures.")
        print("WARNING: If SPF and/or DKIM are not implemented then reports may be")
        print("    received for each email sent.")
        print("Enter: 'y' for yes or 'n' for no.")
        user_input = input("Selection: ")
        if ("y" != user_input and "n" != user_input):
            print("")
            print("Sorry, that is not a valid choice.")
    if ("y" == user_input):
        dmarc_forensic_email_address = input("Forensic email address: ")
        # Get failure reporting option
        user_input = ""
        while "y" != user_input and "n" != user_input:
            print("")
            print("By default DMARC failure reporting is only sent if SPF and DKIM both")
            print("fail alignment.")
            print("We recommend 'yes' so you receive reports if SPF or DKIM fail.")
            print("Would you like to make this change?")
            print("Enter: 'y' for yes or 'n' for no.")
            user_input = input("Selection: ")
            if ("y" != user_input and "n" != user_input):
                print("")
                print("Sorry, that is not a valid choice.")
        if ("y" == user_input):
            dmarc_failure_reporting_option = "; fo=1"


# Check to see if the domain provided is a subdomain. If so, set
# "subdomain_name" to a period followed by what is in "domain_name", but
# without the parent domain portion.
# The preceeding period is needed for the DNS host names.
# Example: "mail.domain.xyz" becomes ".mail"
def setSubdomain():
    global subdomain_name
    global parent_domain_name
    periodCount = domain_name.count('.')
    # If there is more than one period then it is a subdomain.
    if (periodCount > 1):
        # Reverse the domain_name string. This places the parent domain at
        # the beginning and makes it easier to remove.
        tempDomain = domain_name[::-1]
        firstPeriodPosition = tempDomain.find(".")
        secondPeriodPosition = tempDomain.find(".", firstPeriodPosition+1)
        # Set the parent domain name.
        parent_domain_name = tempDomain[:secondPeriodPosition][::-1]
        # Get all characters from the second period's postion on.
        tempDomain = tempDomain[secondPeriodPosition+1:]
        # Reverse the string again to get the characters back in the correct
        # order.
        subdomain_name = "."+tempDomain[::-1]

def printOutput():
    # Print DMARC TXT record information.
    print("")
    print("DMARC DNS RECORD ("+domain_name+")")
    print("Record type: TXT")
    print("Host name:   _dmarc"+subdomain_name)
    print("Value:       v=DMARC1; p="+dmarc_policy, end = '')
    if ("" != dmarc_subdomain_policy):
        print("; sp="+dmarc_subdomain_policy, end = '')
    print(dmarc_failure_reporting_option, end = '')
    print(dmarc_dkim_alignment, end ='')
    print(dmarc_spf_alignment, end = '')
    if ("" != dmarc_aggregate_email_address):
        print("; rua=mailto:"+dmarc_aggregate_email_address, end = '')
    if ("" != dmarc_forensic_email_address):
        print("; ruf=mailto:"+dmarc_forensic_email_address, end = '')
    print("")
    
    # Get domain for where emails are going.
    atPosition = dmarc_aggregate_email_address.find("@")
    aggregate_email_domain = dmarc_aggregate_email_address[atPosition+1:]
    # If aggregate report emails are going to a different domain then print DNS record for that domain.
    if (aggregate_email_domain != domain_name and "" != aggregate_email_domain):
        print("")
        print("DMARC DNS RECORD ("+aggregate_email_domain+")")
        print("Record type: TXT")
        print("Host name:   "+domain_name+"._report._dmarc."+aggregate_email_domain)
        print("Value:       v=DMARC1")

    # Get domain for where emails are going.
    atPosition = dmarc_forensic_email_address.find("@")
    forensic_email_domain = dmarc_forensic_email_address[atPosition+1:]
    # If forensic report emails are going to a different domain then print DNS record for that domain.

    if (forensic_email_domain != domain_name and forensic_email_domain != aggregate_email_domain and "" != forensic_email_domain):
        print("")
        print("DMARC DNS RECORD ("+forensic_email_domain+")")
        print("Record type: TXT")
        print("Host name:   "+domain_name+"._report._dmarc."+forensic_email_domain)
        print("Value:       v=DMARC1")

    # Print SPF TXT record information.
    





if __name__ == "__main__":
    main()