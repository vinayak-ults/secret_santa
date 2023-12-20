import pandas as pd
import random
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import settings


@api_view(["POST"])
def view_pair(request):
    input_file=request.FILES["file"]
    df = pd.read_excel(input_file)
    names = df["Names"].tolist()
    random.shuffle(names)
    pairs = []
    for i in range(len(names)):
        pair = f"{names[i]}-{names[(i + 1) % len(names)]}"
        pairs.append(pair)

    random.shuffle(pairs)
    while any(pair.split('-')[0] == pair.split('-')[1] for pair in pairs):
        random.shuffle(pairs)
    result_df = pd.DataFrame(pairs, columns=["Santa-Recipient"])
    file_name=str(uuid.uuid4())
    file=result_df.to_excel('./static/report/'+file_name+'.xlsx', index=False)
    file_path=settings.FILE_PATH + "/static/report/"+file_name+'.xlsx'

    return Response({"data":pairs,"file_path":file_path})

