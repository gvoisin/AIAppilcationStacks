import asyncio

from chat_app.main_llm import OCITerrenaLLM
from langchain_openai import ChatOpenAI
from oci_openai import OciUserPrincipalAuth
import httpx,os



def build_prompt(llm: OCITerrenaLLM) -> str:
    final_response_content = """
    Dernieres alertes Terrena :
    - filiere: volailles
    - territoire: Vendee
    - statut: en analyse
    - impact: 86000 animaux sous protocole renforce
    - cause: renforcement preventif sanitaire
    """.strip()

    return llm._out_query + f"\n\nContext for question generation:\n{final_response_content}"


def get_suggestion_llm(llm, flag):
    if flag:
        return llm
    else:
        return ChatOpenAI(
            base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
            #base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",

            http_client=httpx.Client(auth=OciUserPrincipalAuth(profile_name=os.getenv("AUTH_PROFILE"))),
                default_headers={
                "opc-compartment-id": os.getenv("COMPARTMENT_ID"),
                "opc-conversation-store-id": "xx"
                },
            api_key=os.getenv('OPENAI_INNO_DEV1'),
            model="openai.gpt-5.4",
            store = False
        )


async def run_async_version(flag):
    llm = OCITerrenaLLM()
    prompt = build_prompt(llm)

    print("\n" + "=" * 80)
    print("EXECUTION ASYNCHRONE (ainvoke)")
    print("=" * 80)
    print("prompt sent to suggestion model:\n")
    print(prompt)
    print("\n=== result ===")

    try:
        suggestions = await get_suggestion_llm(llm._suggestion_out,flag).ainvoke(prompt)
        print("suggestions object:", suggestions)
        print("type:", type(suggestions))
        if hasattr(suggestions, "model_dump_json"):
            print("json:", suggestions.model_dump_json())
    except Exception as exc:
        print("error type:", type(exc).__name__)
        print("error details:", exc)


def run_sync_version(flag):
    llm = OCITerrenaLLM()
    prompt = build_prompt(llm)

    print("\n" + "=" * 80)
    print("EXECUTION SYNCHRONE (invoke)")
    print("=" * 80)
    print("prompt sent to suggestion model:\n")
    print(prompt)
    print("\n=== result ===")

    try:
        suggestions = get_suggestion_llm(llm._suggestion_out,flag).invoke(prompt)
        print("suggestions object:", suggestions)
        print("type:", type(suggestions))
        if hasattr(suggestions, "model_dump_json"):
            print("json:", suggestions.model_dump_json())
    except Exception as exc:
        print("error type:", type(exc).__name__)
        print("error details:", exc)


async def main():
    print ("****** OCI OPENAI TERRENA *******")
    await run_async_version(True)
   # run_sync_version(True)
    
    print ("****** OCI NATIVE TERRENA *******")
    
    await run_async_version(False)
    #run_sync_version(False)


if __name__ == "__main__":
    asyncio.run(main())
