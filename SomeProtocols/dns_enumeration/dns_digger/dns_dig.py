from typing import assert_never
import dns.resolver
import sys
from argparser import argparse
from re import match
import threading
import time
from rich.console import Console
#global identifiers :
console=Console()
accepted_records={'A','AAAA','MX','NS','TXT','CNAME'}
usage="""
NAME
       dns_dig : a powerful script to enumerate all possible dns records


SYNOPSIS
        python3 dns_dig.py  --type={A,AAAA,MX,.....}     domain_name1   domain_name2  .... { Domain names to query }

    
DESCRIPTION
        This script uses the python dns package  to send DNS queries 
        to different DNS records , such as :A , AAAA , MX , NS , CNAME , even the TXT record.
        It also uses the Rich package , to colorize the output.
    
OPTIONS
        The type of record specified must be in upper-case format ,
        available records are : A , AAAA , NS , MX ,CNAME , TXT .
        
        --type=type of record :s
            used to specify the type of record to query.
        
        --help or -h:
            print this manual page.

AUTHOR
        Hussam aljaar <https://github.com/husa45>    

"""
def check_command(command:'str')->'bool':
    """
    this function checks if the command is in the right form :
    i.e:programName --type=r1,r2,r3,...  dn1  dn2  dn3 dn4 ....
    where (r[n] is the type of record ) ,(dn[n] is the domain name to query upon )
    """
    return bool(match(r'^((?:--help|-h)|((?:--type=([A-Z]+,?)+)\s(?:[a-zA-Z0-9.-_]+\s?)+))$',command))
def dns_resolving_handler(domain_name:'str',record_type_list:'list')->'str':
    console.print(f"domain name : {domain_name}\n",style='dark_blue bold on red')
    result=""
    for record in record_type_list:
        if record in accepted_records:
            try:
                answers=dns.resolver.resolve(domain_name,record)
                result+=f"\nrecord type : {record}\nAnswers : \n\n"
                for answer in answers:
                    result+=f"\t{answer}\n"
            except dns.resolver.NoAnswer as E:
                console.print(E.msg,style="red bold")

            except dns.exception.DNSException:
                console.print("#"*60,style='red bold')
                console.print(f"the domain name [blue]{domain_name}[red bold] does not exist",style='red bold')
                console.print("#"*60,style='red bold')
                print()
                return
    console.print(f"{result}\n",style="green bold")
    console.print("*"*136,style='white')
    print()


def main():
    args=sys.argv[1:]
    query_results=[]
    command,command_parts=' '.join(args),None
    command_parts=argparse(command)

    if check_command(command):
        if args[0]=='--help' or args[0]=='-h':
            print(usage,end="",flush=True)
            return
        records_required=command_parts['--type'].split(',')
        domains_to_query=[   part     for part in  command_parts if not part.startswith('--')]
        for domain in domains_to_query:
            thread=threading.Thread(target=dns_resolving_handler,args=(domain,records_required))
            thread.start()
            thread.join()
    else:
       console.print("Invalid Syntax ,try : \n",style='red bold')
       console.print('\tpython3 dns_dig.py  --type={A,AAAA,MX,....}     domain_name1   domain_name2  .... (domain names to query)' )
       raise SystemExit()
if __name__=="__main__":
    main()

