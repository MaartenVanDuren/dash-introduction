#!/bin/bash

/bin/bash -c "source activate meetup_dash && cd ./dash-stock-tickers-demo-app && python app.py" &
/bin/bash -c "source activate meetup_dash3 && cd ./demo2 && python app.py" &
/bin/bash -c "source activate meetup_dash3 && cd ./demo3 && python app.py" &
/bin/bash -c "source activate meetup_dash3 && cd ./demo4 && python app.py" &
/bin/bash -c "source activate meetup_dash3 && cd ./demo5 && python app.py" &
/bin/bash -c "source activate meetup_dash3 && cd ./demo6 && python app.py" &
/bin/bash -c "source activate meetup_dash3 && cd ./demo7 && python app.py" &
/bin/bash -c "source activate meetup_dash3 && cd ./demo8 && python app.py" &
/bin/bash -c "source activate meetup_dash3 && cd ./demo9 && python app.py" &
/bin/bash -c "source activate meetup_dash3 && cd ./demo10 && python app.py" &
/bin/bash -c "source activate meetup_dash3 && cd ./demo11 && python app.py" &


echo "ALL STARTED..."
