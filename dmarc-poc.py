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
#       - Python 3.8.2.
# ****************************************************************************
# History:
# 1 September 2020 - Tim Lansing - Initial creation.
# ****************************************************************************

# Declare global variables.
domain_name = ""
subdomain_name = ""
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
    global dmarc_dkim_alignment = ""
    global dmarc_spf_alignment = ""
    global dmarc_aggregate_email_address = ""
    global dmarc_forensic_email_address = ""

    # Get the domain name.
    print("")
    domain_name = input("Domain name: ")
    setSubdomain()

    # Get the DMARC policy.
    dmarc_policy = ""
    while "" == dmarc_policy:
        print("")
        print("Do you want to monitor your domain, ask to send emails to quarantine")
        print("if they do not pass SPF or DKIM, or ask to reject emails if they do not")
        print("pass SPF or DKIM?")
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

    # Get failure reporting option
    user_input = ""
    while "y" != user_input and "n" != user_input:
        print("")
        print("By default DMARC failure reporting is only sent if SPF and DKIM both")
        print("fail alignment.")
        print("We recommend that you receive reports if SPF or DKIM fail.")
        print("Would you like to make this change?")
        print("Enter: 'y' for yes or 'n' for no.")
        user_input = input("Selection: ")
        if ("y" != user_input and "n" != user_input):
            print("")
            print("Sorry, that is not a valid choice.")
    if ("y" == user_input):
        dmarc_failure_reporting_option = "; fo=1"

    # Get DKIM alignment setting.


    # Get SPF alignment setting.


    # Get aggregate reporting email address.


    # Get forensic reporting email address.



# Check to see if the domain provided is a subdomain. If so, set
# "subdomain_name" to a period followed by what is in "domain_name", but
# without the parent domain portion.
# The preceeding period is needed for the DNS host names.
# Example: "mail.domain.xyz" becomes ".mail"
def setSubdomain():
    global subdomain_name
    periodCount = domain_name.count('.')
    # If there is more than one period then it is a subdomain.
    if (periodCount > 1):
        # Reverse the domain_name string. This places the parent domain at
        # the beginning and makes it easier to remove.
        tempDomain = domain_name[::-1]
        firstPeriodPosition = tempDomain.find(".")
        secondPeriodPosition = tempDomain.find(".", firstPeriodPosition+1)
        # Get all characters from the secon period's psotion on.
        tempDomain = tempDomain[secondPeriodPosition+1:]
        # Reverse the string again to get the characters back in the correct
        # order.
        subdomain_name = "."+tempDomain[::-1]

def printOutput():
    print("")
    print("DMARC DNS RECORD")
    print("Record type: TXT")
    print("Host name:   _dmarc"+subdomain_name)
    print("Value:       v=DMARC1; p="+dmarc_policy, end = '')
    if ("" != dmarc_subdomain_policy):
        print("; sp="+dmarc_subdomain_policy, end = '')
    print(dmarc_failure_reporting_option, end = '')
    print("")
    print("")
    

if __name__ == "__main__":
    main()