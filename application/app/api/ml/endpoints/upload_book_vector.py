from typing import Optional

from fastapi import APIRouter, status, UploadFile, Form, Depends
from fastapi.responses import JSONResponse

from langchain.vectorstores import VectorStore
from fastapi import HTTPException
from app.api.dependencies import get_vector_db
from app.schemas.langchain_schemas.file_schema import FileSchema
from app.schemas.nbic_schema import BookDataSchema
from app.parsers.nbic_json import json_parser


from app.exception.base_exception import (
    file_extension_not_supported,
    vector_index_not_created,
)

router = APIRouter()


@router.post("/upload-book-vector",status_code=status.HTTP_201_CREATED)
async def upload_data(
    book_data: BookDataSchema,
    vector_db: VectorStore = Depends(get_vector_db)
):
    
    """
    Tested data obj
    {
  "id": 0,
  "title": "Friday Forward: Inspiration & Motivation to Help You End Your Week Stronger Than It Started",
  "author_name": "Robert Glaze",
  "description": "Robert Glazer is the founder and CEO of global partner marketing agency, Acceleration Partners, which was recognized as a best place to work by Inc., Fortune, Forbes, Entrepreneur, the Boston Globe, and Glassdoor. He is also the co-founder and Chairman of BrandCycle and was selected as Glassdoor’s #2 small-business CEO in America.\n1. Overnight success is a myth.\nBefore he was a world-famous musician, Ed Sheeran played 300 live shows over four years in London, selling self-published CDs from a rucksack without any real success. Along the way he lost his apartment and resorted to sleeping near a heating duct outside Buckingham Palace. But he didn't give up; in 2010, he bought a one-way ticket to Los Angeles, and eventually, he got his big break. So in addition to his talent, what led him to stratospheric success? He had a clear vision, and a dogged determination to see his dream through, despite failures, fatigue, disappointments, and setbacks. He was willing to take risks and bet on himself.\n2. Strive for excellence in all that you do.\nAnn Miura-Ko's father instilled in her the importance of giving a world-class effort to everything she did, no matter how trivial. So while working as an administrative assistant at Yale, she made crisp copies that people could not discern from the original. She used a label maker for filing, and she made sure to pick the freshest donuts when asked to bring them into the office. A few years into the job, the Dean popped in and said he needed someone to tour his friend Lewis around the engineering school. Miura-Ko gave a great tour and developed a good rapport with the man, who turned out to be Lewis Platt, the CEO of Hewlett-Packard. Platt became a key figure in her professional development, and Ann Miura-Ko went on to become one of the most respected venture capitalists in the country. As her story illustrates, when we commit to being world-class in all that we do, we are choosing our own circumstances, no matter how insignificant they might seem at the time.\n3. Learn to say no with these three strategies.\n\nGive up the guilt. If saying yes to a new request would mean time and attention away from something meaningful that you've already committed to, then saying no is the right thing to do.\nKnow your core values. The next time you get an ask, consider whether fulfilling that need speaks to your core values. Time is both precious and limited, so ensure that your commitments move you toward what is most important to you.\nLeverage templates. When you decide to say no, how you choose to respond can make all the difference. A good rejection letter includes a personal acknowledgement of the individual making the request, an admission of your own need to focus on previous commitments, and a clear statement that you cannot help in this matter. People who get lots of requests often use templates to help them decline politely and consistently. So when you field a new type of request, consider turning your response into a template.\n\n4. The value of putting yourself first.\nBeing selfish and putting yourself first are not the same thing. Being selfish is about believing that the world revolves around you, and not caring about the well-being of others. Putting yourself first, however, is about not compromising on your own needs. To be at our best, for ourselves and for others, we need to make sure that we are living in a way that leaves us happy, healthy, and rested. So prioritize basic needs like sleeping, eating, and exercising. Also try keeping a journal, which promotes self-accountability and mindfulness. Rather than ending up too tired to serve others or enjoy your own achievements, remember to put yourself first.\n5. The importance of resilience.\nOne Sunday in April 1981, the husband of Dr. Mary-Claire King declared that he was leaving her. The following day after work, she discovered that her house had been burglarized. That Friday, King was scheduled to fly to DC to make a case for her first research grant, but she had no one to watch her daughter. So, she called her mentor and told him that she couldn’t make the trip, but he told King to bring her daughter along. He even bought her daughter a plane ticket. In the end, King gave her presentation, received a grant for her research, and later made one of the largest discoveries in breast cancer to date. Mary-Claire King had every reason to quit that week, but the truth is, we all have bad days, weeks, and even months. The question is not whether they will happen, but how we handle them. Will we laugh off our bad luck, or get immobilized by despair? The important thing is to just keep moving forward.",
  "category": "7 Books You Should Have Read By Now",
  "tagName": "Career"
    }

    """
    book_id, docs, metadata  = json_parser(book_data)
    try:
        
        vector_db.insert_document_with_index(book_id, docs, meta=metadata)
        return JSONResponse(
            {
                "message": "vector data inserted created successfully",
            },
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        raise vector_index_not_created