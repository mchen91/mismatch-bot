"""add 25x25 records

Revision ID: 554365813a89
Revises: a67c2dc410d2
Create Date: 2021-02-15 20:36:37.952280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "554365813a89"
down_revision = "a67c2dc410d2"
branch_labels = None
depends_on = None


def upgrade():
    from models import Character, Stage
    from use_cases.aliases import add_char_stage_alias, add_player_alias
    from use_cases.character import get_character_by_name
    from use_cases.player import get_player_by_name
    from use_cases.records import add_record, get_record
    from use_cases.stage import get_stage_by_name

    connection = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=connection)

    frames_raw = """787	583	215	485	570	530	502	559	227	455	716	746	797	623	581	476	441	0	472	651	0	283	193	536	379
848	477	178	490	512	521	478	532	227	445	660	735	659	567	507	398	416	559	436	646	805	299	178	534	400
765	680	193	533	674	602	504	563	236	465	683	712	681	761	691	641	507	0	550	755	733	337	209	644	413
1045	709	238	489	656	0	567	641	290	580	828	902	872	687	681	624	547	0	510	765	0	449	232	695	412
875	734	209	594	568	674	576	678	231	504	642	962	897	687	497	419	552	1077	546	799	555	364	182	683	420
835	634	173	483	593	433	501	574	246	446	703	772	761	587	547	452	465	0	458	631	0	338	205	580	435
967	732	239	560	598	0	503	669	301	513	751	877	824	651	675	671	409	0	535	717	790	407	193	681	398
786	630	221	476	542	549	400	445	235	466	572	718	697	644	484	539	384	895	379	559	0	356	149	525	355
0	899	255	582	851	598	631	703	282	587	819	1096	954	763	706	768	597	0	705	831	0	458	178	688	487
469	343	147	419	420	414	333	357	230	298	402	599	391	516	448	448	282	0	315	496	371	262	117	502	283
478	346	93	377	360	365	225	281	227	366	384	688	412	571	430	454	239	0	308	422	305	237	101	412	318
1018	720	235	511	627	586	572	665	289	552	759	779	825	670	642	427	532	0	553	764	987	407	197	715	517
1017	589	239	595	684	0	499	653	287	511	763	864	582	688	616	543	531	0	560	707	0	414	197	506	421
1077	797	261	641	646	702	631	719	252	492	725	959	896	689	716	630	551	0	571	831	749	478	244	763	478
598	520	178	503	445	529	495	529	227	444	517	682	660	659	453	346	430	684	432	654	559	330	145	538	392
927	530	196	560	475	501	499	574	243	479	651	754	613	605	673	360	414	819	535	593	969	396	173	492	402
527	383	157	307	379	356	405	407	210	237	415	482	574	320	330	340	210	732	328	400	402	242	123	418	327
433	349	147	316	295	298	359	359	203	234	360	359	535	287	289	284	227	291	248	309	274	246	115	357	320
870	583	193	479	436	449	522	478	239	411	563	592	736	459	419	381	449	670	328	477	886	297	170	595	433
658	452	191	447	385	434	448	394	223	346	468	550	564	425	419	359	345	0	327	410	529	281	146	476	317
1054	729	237	567	659	649	599	695	272	512	706	973	942	647	679	733	544	1108	522	816	440	418	235	655	505
692	580	202	468	476	499	475	501	239	400	512	688	691	582	500	474	407	640	406	603	682	273	148	539	317
776	573	223	501	527	480	501	538	231	415	531	698	683	614	571	430	442	0	433	661	0	345	169	604	309
890	599	215	517	567	525	522	567	216	447	583	790	779	623	535	572	456	0	419	613	779	354	172	497	357
940	623	206	477	534	564	520	595	218	479	598	829	776	590	578	568	465	0	446	699	0	297	188	586	317"""
    videos_raw = """https://www.youtube.com/watch?v=7lNtSq50NHo	https://www.youtube.com/watch?v=GK6WgnNKphg	https://www.youtube.com/watch?v=gXTQLU1R_zM	https://www.youtube.com/watch?v=7trfinFysLM	https://www.youtube.com/watch?v=tO0qBNqH7jk	https://www.youtube.com/watch?v=JzZMKfg31Fk	https://www.youtube.com/watch?v=Hdain4KDv1c	https://www.youtube.com/watch?v=QfwvRxLdIas	https://www.youtube.com/watch?v=t7hkK2BIYzI	https://www.youtube.com/watch?v=Padr42zMsoA	https://www.youtube.com/watch?v=TC4zYAfGB4o	https://www.youtube.com/watch?v=Plm_5O1U758	https://www.youtube.com/watch?v=qHkZlc6Fcc8	https://www.youtube.com/watch?v=6mvzq1PHzVk	https://www.youtube.com/watch?v=83mWk3B5t3g	https://www.youtube.com/watch?v=pIM8YkTmins	https://www.youtube.com/watch?v=S71m5M2415o	N/A	https://www.youtube.com/watch?v=zZNxMHF58w8	https://www.youtube.com/watch?v=JgMPbTdpH54	N/A	https://www.youtube.com/watch?v=2QlRgSg9amo	https://www.youtube.com/watch?v=IRwawQr3drU	https://www.youtube.com/watch?v=148P8iGfRa4	https://www.youtube.com/watch?v=2M5iHK9BGZA
https://www.youtube.com/watch?v=2rgQIgweCjE	https://www.youtube.com/watch?v=L52InTj1kuk	https://www.youtube.com/watch?v=YXmqV-0Nul4	https://www.youtube.com/watch?v=tTLkWqOkJzk	https://www.youtube.com/watch?v=JTObCroXehU	https://www.youtube.com/watch?v=WzouRoday0A	https://www.youtube.com/watch?v=4Jd8dZM5x6w	https://www.youtube.com/watch?v=2rgQIgweCjE&t=86s	https://www.youtube.com/watch?v=ehb07oFyqq4	https://www.youtube.com/watch?v=QCwS7QpNn_c	https://www.youtube.com/watch?v=2rgQIgweCjE&t=117s	https://www.youtube.com/watch?v=2rgQIgweCjE&t=131s	https://www.youtube.com/watch?v=aaw2Dk1MlzU	https://www.youtube.com/watch?v=2rgQIgweCjE&t=161s	https://www.youtube.com/watch?v=csanzdqk9yw	https://www.youtube.com/watch?v=2rgQIgweCjE&t=187s	https://www.youtube.com/watch?v=qkLSr1hJ0CA	https://www.youtube.com/watch?v=c4KEM3GRxP8	https://www.youtube.com/watch?v=oe9UCF1fBoU	https://www.youtube.com/watch?v=J7kjLMKTO_0	https://www.youtube.com/watch?v=FqwkV6OCPZM	https://www.youtube.com/watch?v=L_bwf1meXKo	https://www.youtube.com/watch?v=2rgQIgweCjE&t=258s	https://www.youtube.com/watch?v=6PE3q6AGfXo	https://www.youtube.com/watch?v=nT80gNrRnEM
https://www.youtube.com/watch?v=h9jcb-caI44	https://www.youtube.com/watch?v=wf7ckXdRvkc	https://www.youtube.com/watch?v=kq1zJoKxkuM	https://www.youtube.com/watch?v=T2-QWhm_KO8	https://www.youtube.com/watch?v=TR4JeyFO65I	https://www.youtube.com/watch?v=xkQyKYnJaVw	https://www.youtube.com/watch?v=QAnC52S3Li0	https://www.youtube.com/watch?v=uLnoFHbx90U	https://www.youtube.com/watch?v=Odh_hv3FOSw	https://www.youtube.com/watch?v=Cg36tDpAtiY	https://www.youtube.com/watch?v=NfgAOYlivY0	https://www.youtube.com/watch?v=1ccgDvUIRkU	https://www.youtube.com/watch?v=apDrTBAd8Zo	https://www.youtube.com/watch?v=kxXEQS3992k	https://www.youtube.com/watch?v=5pXOjN_WXtk	https://www.youtube.com/watch?v=NMfDruGBpgY	https://www.youtube.com/watch?v=lhuunJmmGLY	N/A	https://www.youtube.com/watch?v=DlLHFO3W2aw	https://www.youtube.com/watch?v=zxbx1SokDsY	https://www.youtube.com/watch?v=fFwaesMfFYA	https://www.youtube.com/watch?v=UH-V4_0R62s	https://www.youtube.com/watch?v=p8QXSRfoMJQ	https://www.youtube.com/watch?v=gbnlzFKktBE	https://www.youtube.com/watch?v=fwZpr9loTX0
https://www.youtube.com/watch?v=I-DXEZ_JHBQ	https://www.youtube.com/watch?v=ZqyaclFr6i0	https://www.youtube.com/watch?v=-hG10yxiJeY	https://www.youtube.com/watch?v=tR3Hq2f8oUY	https://www.youtube.com/watch?v=9bzp5ymWFvc	N/A	https://www.youtube.com/watch?v=YxY1BtzyTiU	https://youtu.be/Zn5mEFUbvCg?t=79	https://www.youtube.com/watch?v=0uf9cYMU1_w	https://www.youtube.com/watch?v=BV0xMF8fV8M	https://www.youtube.com/watch?v=LX2yjAZ12Xw	https://www.youtube.com/watch?v=0qFfzvkykQQ	https://www.youtube.com/watch?v=hCzW_DWegsk	https://www.youtube.com/watch?v=EgISgvRdFQ0	https://www.youtube.com/watch?v=YZXgJJvryrw	https://www.youtube.com/watch?v=dhNYnf2Bu9U	https://www.youtube.com/watch?v=Cej1SpLnmgk	N/A	https://www.youtube.com/watch?v=-KbraYVPeeI	https://www.youtube.com/watch?v=dwCZDvWN1CQ	N/A	https://www.youtube.com/watch?v=T8kFuqrjk1s	https://www.youtube.com/watch?v=jrQ67YVLAa0	https://www.youtube.com/watch?v=HpR42mNRwkA	https://www.youtube.com/watch?v=QVVkqIADIwk
https://www.youtube.com/watch?v=UPGtWfHZhKg	https://www.youtube.com/watch?v=sBs3MdNDelM	https://youtu.be/lfPxiK2CbMY?t=19	https://www.youtube.com/watch?v=R2GkTMiD8IQ	https://www.youtube.com/watch?v=kVaG0PSzmrQ	https://youtu.be/2Sj9wV8jlOw?t=42	https://www.youtube.com/watch?v=68qK07bYzp0	https://www.youtube.com/watch?v=r3lCx90q1PQ	https://www.youtube.com/watch?v=Lo5nNJ4d9LA	https://www.youtube.com/watch?v=bgP709-h6bY	https://www.youtube.com/watch?v=LQLPWJHxels	https://www.youtube.com/watch?v=0d14RZjO6v8	https://www.youtube.com/watch?v=QuxhHmWHQ1k	https://www.youtube.com/watch?v=iJBP7gF50fs	https://www.youtube.com/watch?v=JfQZAtQodXE	https://www.youtube.com/watch?v=RRweGBqCmfA	https://www.youtube.com/watch?v=_FxLF4n1uxw	https://www.youtube.com/watch?v=f4n3KUQNSJQ	https://www.youtube.com/watch?v=OP5Kc0hGfVo	https://www.youtube.com/watch?v=K1MLGUo0iBE	https://www.youtube.com/watch?v=iSAPQSJ7jzA	https://www.youtube.com/watch?v=palz2WH4FGs	https://www.youtube.com/watch?v=yJ2oC3pZstk	https://www.youtube.com/watch?v=3oaTTEpPJO0	https://www.youtube.com/watch?v=YBCYY6R5DTk
https://www.youtube.com/watch?v=Yqip3A6pjtU	https://www.youtube.com/watch?v=xUH0sv4f6z0	https://www.youtube.com/watch?v=3hsJqLkR_rE	https://www.youtube.com/watch?v=gILlUUpBvbI	https://www.youtube.com/watch?v=rTz0LJnr2W4	https://www.youtube.com/watch?v=LXUBF0GuWfQ	https://www.youtube.com/watch?v=nowBl_q5w3w	https://www.youtube.com/watch?v=AkWER7zd4_8	https://www.youtube.com/watch?v=BqaF4jp7mMw	https://www.youtube.com/watch?v=C_SMwS0bLRo	https://www.youtube.com/watch?v=LExTlb9mgbs	https://www.youtube.com/watch?v=ZUK1tTETDTQ	https://www.youtube.com/watch?v=Xd-FhyQpeDQ	https://www.youtube.com/watch?v=I6_eaxG6Sj0	https://www.youtube.com/watch?v=mVrlS0Uq0F4	https://www.youtube.com/watch?v=HZCf-yzFEr4	https://www.youtube.com/watch?v=Ty0QLiGXpx4	N/A	https://www.youtube.com/watch?v=Ktw0FaCM3nY	https://www.youtube.com/watch?v=5DdtGLEIOmQ	N/A	https://www.youtube.com/watch?v=fMuFutsHURA	https://www.youtube.com/watch?v=yJUi2Lt2rnA	https://www.youtube.com/watch?v=fjnupMz0wD8	https://www.youtube.com/watch?v=XMj5cLxJ4xQ
https://www.youtube.com/watch?v=29LYgrs1eII	https://www.youtube.com/watch?v=_juZKSyxql8	https://www.youtube.com/watch?v=yrId2C7fKh8	https://www.youtube.com/watch?v=5gPEyNGnWek	https://www.youtube.com/watch?v=puogjWK5WfA	N/A	https://www.youtube.com/watch?v=ccpa4hs66OU	https://www.youtube.com/watch?v=LqOBzY4EYgQ	https://www.youtube.com/watch?v=pxJ50Nskl4s	https://www.youtube.com/watch?v=OasN_u0LJmY	https://www.youtube.com/watch?v=21Vws7YtID8	https://www.youtube.com/watch?v=yI4dxZlHJ1A	https://www.youtube.com/watch?v=RRk5hVCAoJY	https://www.youtube.com/watch?v=5RiFtW3xFdM	https://www.youtube.com/watch?v=xxO6r62YJnk	https://www.youtube.com/watch?v=2FjR67n9ysI	https://www.youtube.com/watch?v=ECqul0Vlo1U	N/A	https://www.youtube.com/watch?v=NipcJuOwgKo	https://www.youtube.com/watch?v=FmZKXjyMzio	https://www.youtube.com/watch?v=1yq6HgRg0Bw	https://www.youtube.com/watch?v=l9bnFpBXRhw	https://www.youtube.com/watch?v=84O0J_uIHpk	https://www.youtube.com/watch?v=PYaRrj8pcbY	https://www.youtube.com/watch?v=3ioB6TJeKRY
https://www.youtube.com/watch?v=gPe3QAFAgOU	https://www.youtube.com/watch?v=we9H0CyTp58	https://www.youtube.com/watch?v=c57m0czMHHI	https://www.youtube.com/watch?v=d9CKW7jtI24	https://www.youtube.com/watch?v=q7OEwKuFs-E	https://www.youtube.com/watch?v=p48NWkK2RPk	https://www.youtube.com/watch?v=M9wV6pMKG_k	https://www.youtube.com/watch?v=6uGEDxKbu1w	https://www.youtube.com/watch?v=jl2qghtfnRo	https://www.youtube.com/watch?v=MMB1YsKCfJw	https://www.youtube.com/watch?v=vVfDpTKWwro	https://www.youtube.com/watch?v=LO25pcSYCc0	https://www.youtube.com/watch?v=E3XWQrpcPYg	https://www.youtube.com/watch?v=AJbafmGwraA	https://www.youtube.com/watch?v=A66GKrSYjxM	https://www.youtube.com/watch?v=imdLBefxYcs	https://www.youtube.com/watch?v=XQeN18rv1mo	https://www.youtube.com/watch?v=Bu73VOrFqz8	https://www.youtube.com/watch?v=v_MbEm6Nyqg	https://www.youtube.com/watch?v=BKpI5VBlmSc	N/A	https://www.youtube.com/watch?v=HJ9iX6toMDo	https://www.youtube.com/watch?v=HYWTFrTfNDw	https://www.youtube.com/watch?v=IljCXdUUQRo	https://www.youtube.com/watch?v=-YN1ZcMb0_U
N/A	https://www.youtube.com/watch?v=TjogMhf8B7Y	https://www.youtube.com/watch?v=bpqc3Zy157o	https://www.youtube.com/watch?v=sTloshZcUbs	https://www.youtube.com/watch?v=UCxyj944HqA	https://www.youtube.com/watch?v=z3RhaMc7SdI	https://www.youtube.com/watch?v=0ShqNSAnuBo	https://www.youtube.com/watch?v=tcMIwUdiPhc	https://www.youtube.com/watch?v=lFBiydeaIVM	https://www.youtube.com/watch?v=Qpz7J44-QIs	https://www.youtube.com/watch?v=r2mWJLJGTXg	https://www.youtube.com/watch?v=xDHhIcZ3CNo	https://www.youtube.com/watch?v=6Y2xHDsTczU	https://www.youtube.com/watch?v=wuQU5wNWIsE	https://www.youtube.com/watch?v=KXJ8w0LVP00	https://www.youtube.com/watch?v=t8YwyDxr2DQ	https://www.youtube.com/watch?v=6MxkFFVV5aQ	N/A	https://www.youtube.com/watch?v=WIwihIUAWG0	https://www.youtube.com/watch?v=0ow8SvCRbdQ	N/A	https://www.youtube.com/watch?v=Y0pmJWZiIio	https://www.youtube.com/watch?v=iKeyT_zLzxc	https://www.youtube.com/watch?v=ZpzPxFPTFZE	https://www.youtube.com/watch?v=S4Yv0ZBDnl4
https://www.youtube.com/watch?v=zEP0HECDd8Q	https://www.youtube.com/watch?v=DXtP1gZmxq4	https://www.youtube.com/watch?v=OxUKz642jUA	https://www.youtube.com/watch?v=DQekC1MukdM	https://www.youtube.com/watch?v=9IJ-prLWQEQ	https://www.youtube.com/watch?v=9GNcToGckuY	https://www.youtube.com/watch?v=EBl8LHB5-bw	https://www.youtube.com/watch?v=3RjNcTqHTV8	https://www.youtube.com/watch?v=JWnrETRYK2c	https://www.youtube.com/watch?v=zqTCZYpz_dI	https://www.youtube.com/watch?v=0VQ2aBCQZ-Y	https://www.youtube.com/watch?v=5zqwUrh2EgU	https://clips.twitch.tv/CrackyCrazyCobraGivePLZ	https://www.youtube.com/watch?v=1gmyZVrYlP4	https://www.youtube.com/watch?v=JWeoWYG5Yq4	https://www.youtube.com/watch?v=mKHcmBkIcQM	https://www.youtube.com/watch?v=XkP2VcgSiYs	N/A	https://www.youtube.com/watch?v=_pAqKwF-1XU	https://www.youtube.com/watch?v=DY6XPg9x964	https://www.youtube.com/watch?v=77CKIoZWeKE	https://www.youtube.com/watch?v=b7iLcHOo3uo	https://www.youtube.com/watch?v=YEvTu9cBi18	https://www.youtube.com/watch?v=vV_c9Gyg61g	https://www.youtube.com/watch?v=cMj9-LjBPB4
https://www.youtube.com/watch?v=2Wegc81UTFk	https://www.youtube.com/watch?v=2-4HZYlF2_g	https://www.youtube.com/watch?v=7dab8S8bkEs	https://www.youtube.com/watch?v=A3avQubJdgQ	https://www.youtube.com/watch?v=fwlqP5DbowI	https://www.youtube.com/watch?v=h8EqU_a3SNw	https://www.youtube.com/watch?v=_Ig3c-gTrtk	https://www.youtube.com/watch?v=pgJGw6NNcow	https://www.youtube.com/watch?v=aa4hZGnlUTk	https://www.youtube.com/watch?v=vpVr2gNSGyU	https://www.youtube.com/watch?v=gh7vZBbvMlw	https://www.youtube.com/watch?v=cxx9GWQn3sQ	https://www.youtube.com/watch?v=O6C3JxrBWWY	https://www.youtube.com/watch?v=RsBVzW3bsNM	https://www.youtube.com/watch?v=svlAmr5nyFU	https://www.youtube.com/watch?v=SHv4ipl2r4k	https://www.youtube.com/watch?v=QsNHhlSaAP8	N/A	https://clips.twitch.tv/CooperativeMoralLyrebirdCmonBruh	https://www.youtube.com/watch?v=PvOkh9kXDds	https://www.youtube.com/watch?v=YuZ8V4hCI_I	https://www.youtube.com/watch?v=GEknDriZCms	https://www.youtube.com/watch?v=0lf8NaZEl0E	https://www.youtube.com/watch?v=UnMGCwXSQdk	https://www.youtube.com/watch?v=xcn1vMKLieo
https://www.youtube.com/watch?v=RhqI18DyoqY	https://www.youtube.com/watch?v=YvfVVCaXI1w	https://www.youtube.com/watch?v=Yh92EyrD1-M	https://www.youtube.com/watch?v=8IOg0q_0cEY	https://www.youtube.com/watch?v=kFLJMFtqnOw	https://www.youtube.com/watch?v=tOm6wf76hkE	https://www.youtube.com/watch?v=SMpMr9AzOjE	https://www.youtube.com/watch?v=22pnF1JC_Lo	https://www.youtube.com/watch?v=rU1kgImEGtE	https://www.youtube.com/watch?v=n4y4-v3rpRc	https://www.youtube.com/watch?v=0RmEeVKLo0U	https://www.youtube.com/watch?v=ztuOokjPXlU	https://www.youtube.com/watch?v=UjW8HAhZZcY	https://www.youtube.com/watch?v=lp-DLoiX024	https://www.youtube.com/watch?v=F8PUWk2-X5I	https://www.youtube.com/watch?v=wulz27Bksfo	https://www.youtube.com/watch?v=Izz9AmS-88Q	N/A	https://www.youtube.com/watch?v=OwY8SH45B7I	https://www.youtube.com/watch?v=nZIFHR1FJ4g	https://www.youtube.com/watch?v=5u8S5q-ix84	https://www.youtube.com/watch?v=9Ls4uQwfX1Y	https://www.youtube.com/watch?v=BOLdP0hWvEI	https://www.youtube.com/watch?v=UJNEmnMYmXA	https://www.youtube.com/watch?v=XZW7yzoicm4
https://www.youtube.com/watch?v=-Ct-Xi2b14w	https://www.youtube.com/watch?v=ctKXxjb_awQ	https://www.youtube.com/watch?v=ZN9HUkflZ6I	https://www.youtube.com/watch?v=tMadLl3Xpe8	https://www.youtube.com/watch?v=JVtDBXOWKL4	N/A	https://www.youtube.com/watch?v=EXXwFRse3tQ	https://www.youtube.com/watch?v=Ec5LZE2kL-c	https://www.youtube.com/watch?v=9kvoI09NKOI	https://www.youtube.com/watch?v=1c3rIB0ZfAs	https://www.youtube.com/watch?v=MxWTUtKATL0	https://www.youtube.com/watch?v=3Fkuw2mA6lI	https://www.youtube.com/watch?v=XADRvLewY8w	https://www.youtube.com/watch?v=dCA1Wh5imWE	https://www.youtube.com/watch?v=LWEjjCEsEj8	https://www.youtube.com/watch?v=ww6a_Jw-dVE	https://www.youtube.com/watch?v=VDoQLTD78Fs	N/A	https://www.youtube.com/watch?v=HPskgrRWUGk	https://www.youtube.com/watch?v=cd4fNwurqCM	N/A	https://www.youtube.com/watch?v=ZrclOzsYPr8	https://www.youtube.com/watch?v=9acuQxwxxlc	https://www.youtube.com/watch?v=xafPVdA7wN8	https://www.youtube.com/watch?v=rbUEAHa_PY0
https://www.youtube.com/watch?v=sJf2e0BJqIY	https://www.youtube.com/watch?v=rIvjDVWctFI	https://www.youtube.com/watch?v=QyWupUT5H1A	https://www.youtube.com/watch?v=whYaDZXh9Qc	https://www.youtube.com/watch?v=nUzGH3TgtUo	https://www.youtube.com/watch?v=tZElleImoOY	https://www.youtube.com/watch?v=xrGXOwiXXxk	https://www.youtube.com/watch?v=rkbWhYKl6wQ	https://www.youtube.com/watch?v=kIIFc6d_NEg	https://www.youtube.com/watch?v=tJwz2p2GYWU	https://www.youtube.com/watch?v=Bs-zyl2E6do	https://www.youtube.com/watch?v=0NE86xa2VLM	https://www.youtube.com/watch?v=TOdeKol0snE	https://www.youtube.com/watch?v=GDIrI8Jcnu0	https://www.youtube.com/watch?v=ImXY5Hfm8mc	https://www.youtube.com/watch?v=S7RtyMvBcRU	https://www.youtube.com/watch?v=ov2x6lM2Nns	N/A	https://www.youtube.com/watch?v=aAy3WUFIOo4	https://www.youtube.com/watch?v=4KNziOGkqGg	https://www.youtube.com/watch?v=cCU3DJOTPgc	https://www.youtube.com/watch?v=LYGWjPH5tcA	https://www.youtube.com/watch?v=t6IvMVhK5o8	https://www.youtube.com/watch?v=sZxDppKHiZg	https://www.youtube.com/watch?v=asGLc59Jzm4
https://www.youtube.com/watch?v=M39VDHDaFAw	https://www.youtube.com/watch?v=mit9XGV6PX4	https://www.youtube.com/watch?v=AjkbNKlS6H4	https://www.youtube.com/watch?v=R7n0WLtpIfs	https://www.youtube.com/watch?v=_FLsF1GCH_M	https://www.youtube.com/watch?v=fZvLnu139cQ	https://www.youtube.com/watch?v=xHk0yMvGbvk	https://www.youtube.com/watch?v=s8UJBEnKBno	https://www.youtube.com/watch?v=KTICHiuVY_c	https://www.youtube.com/watch?v=8aHynqFIgAI	https://www.youtube.com/watch?v=PhKvZeJ0bMI	https://www.youtube.com/watch?v=rns2jmMqxxo	https://www.youtube.com/watch?v=hktolVVO1rk	https://www.youtube.com/watch?v=RNcTJBlr1ZQ	https://www.youtube.com/watch?v=kFwSI7PMLNk	https://www.youtube.com/watch?v=9cVSImadCYg	https://www.youtube.com/watch?v=WMaFacJDITA	https://www.youtube.com/watch?v=DcMSwOMkKhI	https://www.youtube.com/watch?v=ujNYTQpxxD4	https://www.youtube.com/watch?v=WGEDJ7lkr4E	https://www.youtube.com/watch?v=TKtVsr-vE6w	https://www.youtube.com/watch?v=oISLO1QWrSE	https://www.youtube.com/watch?v=PvrrTAIXA_A	https://www.youtube.com/watch?v=ecOBvu-y8qw	https://www.youtube.com/watch?v=53uF8JybCa0
https://www.youtube.com/watch?v=Yh5W9s_WA_g	https://www.youtube.com/watch?v=dWErJI7Exzk	https://www.youtube.com/watch?v=Rgnbh57gm-g	https://youtu.be/Pk7IaR_CL4w?t=37	https://www.youtube.com/watch?v=PzgeIuQQutY	https://youtu.be/Pk7IaR_CL4w?t=60	https://youtu.be/Pk7IaR_CL4w?t=71	https://www.youtube.com/watch?v=OjgLAWq4k4U	https://www.youtube.com/watch?v=aOb4y8Oj-84	https://youtu.be/Pk7IaR_CL4w?t=101	https://youtu.be/Pk7IaR_CL4w?t=112	https://youtu.be/Pk7IaR_CL4w?t=125	https://youtu.be/Pk7IaR_CL4w?t=140	https://youtu.be/Pk7IaR_CL4w?t=154	https://youtu.be/Pk7IaR_CL4w?t=166	https://www.youtube.com/watch?v=Sp6ojv_c9ks	https://youtu.be/Pk7IaR_CL4w?t=190	https://youtu.be/Pk7IaR_CL4w?t=200	https://youtu.be/Pk7IaR_CL4w?t=216	https://www.youtube.com/watch?v=6MQyBmscItM	https://www.youtube.com/watch?v=2vljcuawHwo	https://youtu.be/Pk7IaR_CL4w?t=263	https://youtu.be/Pk7IaR_CL4w?t=273	https://youtu.be/Pk7IaR_CL4w?t=279	https://youtu.be/Pk7IaR_CL4w?t=290
https://twitter.com/Savestate/status/1094284626699395072	https://twitter.com/Savestate/status/1002748314457202688	https://www.youtube.com/watch?v=E7plcp3-PNw	https://twitter.com/Savestate/status/1138412737682391046	https://twitter.com/Savestate/status/989634698392502274	https://twitter.com/Savestate/status/988194536458457089	https://twitter.com/Savestate/status/1002763166563143681	https://twitter.com/Savestate/status/1133938083286704129	https://twitter.com/Savestate/status/1058932199704219648	https://twitter.com/Savestate/status/993645942376222720	https://twitter.com/Savestate/status/993255044651929600	https://twitter.com/Savestate/status/1134953164673826817	https://twitter.com/Savestate/status/1137900814176067584	https://twitter.com/Savestate/status/1010994055281561601	https://twitter.com/Savestate/status/1058821178415038468	https://twitter.com/Savestate/status/1051200393915588613	https://www.youtube.com/watch?v=2E0qyX5jM2I	https://twitter.com/Savestate/status/984895162793984001	https://twitter.com/Savestate/status/1058803586568781824	https://twitter.com/Savestate/status/1164602932475637760	https://twitter.com/Savestate/status/1286090236389396480	https://twitter.com/Savestate/status/1286096592253132800	https://twitter.com/Savestate/status/1002729912409747456	https://twitter.com/Savestate/status/1137828392613683205	https://twitter.com/Savestate/status/1094228723098894336
https://www.youtube.com/watch?v=eGqaxmqMYbc	https://www.youtube.com/watch?v=XM2btPzyOWo	https://www.youtube.com/watch?v=oM9n9XnbTpo	https://www.youtube.com/watch?v=JpWJ_4xlGjk	https://www.youtube.com/watch?v=8n8O9LDXOVY	https://www.youtube.com/watch?v=gDW25OFHVko	https://www.youtube.com/watch?v=g_BCqFFU09w	https://www.youtube.com/watch?v=W8HCuT6SjXg	https://www.youtube.com/watch?v=gclXdjBTF-E	https://www.youtube.com/watch?v=2fvQI1vVuCE	https://www.youtube.com/watch?v=7UV-4IeoaNQ	https://www.youtube.com/watch?v=5pFcHAE9Yrk	https://www.youtube.com/watch?v=JjwtM9zh8SM	https://www.youtube.com/watch?v=f-GPVeJqJio	https://www.youtube.com/watch?v=68pelq7WrXk	https://www.youtube.com/watch?v=S1gb9-SOVmo	https://www.youtube.com/watch?v=6S0xOWU4NJM	https://www.youtube.com/watch?v=TkwWcNeG-JE	https://www.youtube.com/watch?v=bK0iLy_gmUs	https://www.youtube.com/watch?v=CDAAZuewBf0	https://www.youtube.com/watch?v=FnPU2BuNJMk	https://www.youtube.com/watch?v=9EOHBd8R88Q	https://www.youtube.com/watch?v=aC8aqqPJiig	https://www.youtube.com/watch?v=OWN5GKX-rU0	https://www.youtube.com/watch?v=ZqFskHNPkWE
https://www.youtube.com/watch?v=vJuQEOA4ZCw	https://www.youtube.com/watch?v=zYIrQ7rz2Ww	https://www.youtube.com/watch?v=DNjzDFMlHG0	https://www.youtube.com/watch?v=E4nm_F9NAss	https://www.youtube.com/watch?v=H9jja6AjBaU	https://www.youtube.com/watch?v=Bzds1HPYoUM	https://www.youtube.com/watch?v=pxa7oClh5jE	https://www.youtube.com/watch?v=e7LxK43JAAM	https://www.youtube.com/watch?v=E1coxZq8ySQ	https://www.youtube.com/watch?v=NWeRoQ9Wp08	https://www.youtube.com/watch?v=iLVfOYZyhnk	https://www.youtube.com/watch?v=mlxYqgPKJXo	https://www.youtube.com/watch?v=LHSrSsjLj1Q	https://www.youtube.com/watch?v=JfJs7_yi0rw	https://www.youtube.com/watch?v=UyWq5CZoxKk	https://www.youtube.com/watch?v=h3XXph49xtk	https://www.youtube.com/watch?v=MsKO5e4e5sM	https://www.youtube.com/watch?v=8cKgbNQiFS4	https://www.youtube.com/watch?v=6j8mfKmw458	https://www.youtube.com/watch?v=MBCha68F1vo	https://www.youtube.com/watch?v=5UauL1-1JP4	https://www.youtube.com/watch?v=xi1FqrfQSgA	https://www.youtube.com/watch?v=bo44Y8Yowes	https://www.youtube.com/watch?v=G27ZiUD65Ww	https://www.youtube.com/watch?v=fpzTT0j6Vvg
https://www.youtube.com/watch?v=CD9jeevIUzo	https://www.youtube.com/watch?v=Np4yexcsRzk	https://www.youtube.com/watch?v=eHojMTKx2go	https://www.youtube.com/watch?v=XkL2SfPQxjQ	https://www.youtube.com/watch?v=vVTW9xgjL6s	https://www.youtube.com/watch?v=IuilSUTO3M8	https://www.youtube.com/watch?v=1hgMonUJCb8	https://www.youtube.com/watch?v=l2wnfPKkQ94	https://www.youtube.com/watch?v=_HqcAQewCVU	https://www.youtube.com/watch?v=FZ8LB8bJxfw	https://www.youtube.com/watch?v=Mynn-YG1kGs	https://www.youtube.com/watch?v=2zv79PiKIqE	https://www.youtube.com/watch?v=oOooLGmhygY	https://www.youtube.com/watch?v=8G7UPqql-as	https://www.youtube.com/watch?v=VUGmdNbW1zo	https://www.youtube.com/watch?v=H8pV-X3m0Xw	https://www.youtube.com/watch?v=fkokgKyIbYM	N/A	https://www.youtube.com/watch?v=iOU1Zpb8K7Q	https://www.youtube.com/watch?v=qqwHdsg2FJY	https://www.youtube.com/watch?v=khqP5qGMWQc	https://www.youtube.com/watch?v=UTZKUcgrLiE	https://www.youtube.com/watch?v=x07gKSrGKm0	https://www.youtube.com/watch?v=0lU5-olJgNY	https://www.youtube.com/watch?v=tbLLkwQCkTU
https://www.youtube.com/watch?v=yNjgOfGi20U	https://www.youtube.com/watch?v=oSixB9YopwA	https://www.youtube.com/watch?v=8G2WtqAMKFQ	https://www.youtube.com/watch?v=eKrhC9mmHP0	https://www.youtube.com/watch?v=oWBAH89ptGs	https://www.youtube.com/watch?v=CGjPiUiAO1g	https://www.youtube.com/watch?v=yW_SeNWLFYM	https://www.youtube.com/watch?v=3osknFn0rWo	https://www.youtube.com/watch?v=RdRYs64U5tA	https://www.youtube.com/watch?v=UnIv_vUBvy8	https://www.youtube.com/watch?v=iqVr5WkmSC4	https://www.youtube.com/watch?v=JbxReYGXx7Y	https://www.youtube.com/watch?v=DSEd0AdHTFQ	https://www.youtube.com/watch?v=qXfx3ig8EDc	https://www.youtube.com/watch?v=pnn43ulBk1c	https://www.youtube.com/watch?v=98hzRBepckU	https://www.youtube.com/watch?v=Fu-WS17i0BI	https://www.youtube.com/watch?v=Go2x0KJWU9Q	https://www.youtube.com/watch?v=xyPw6dACBzE	https://www.youtube.com/watch?v=RAiS_MAtuis	https://www.youtube.com/watch?v=YOdUF7zPpDg	https://www.youtube.com/watch?v=GhWShmgkpS0	https://www.youtube.com/watch?v=fKSJbwUwUz4	https://www.youtube.com/watch?v=N10-xMZfgW0	https://www.youtube.com/watch?v=2NSl__4Fo3A
https://www.youtube.com/watch?v=i-aAbeS2_b8	https://www.youtube.com/watch?v=KDzMPg_B2uE	https://www.youtube.com/watch?v=eJyxBm6Kj6Q	https://www.youtube.com/watch?v=gsTNadm8kHM	https://www.youtube.com/watch?v=6ewdi4xBWtU	https://www.youtube.com/watch?v=tPUqzy9fsX0	https://www.youtube.com/watch?v=MuV30khGg7c	https://www.youtube.com/watch?v=_-4wI0Ewv5M	https://www.youtube.com/watch?v=XTv5HcRwEpE	https://www.youtube.com/watch?v=z5NmNzw-leM	https://www.youtube.com/watch?v=LQHJoMA0gow	https://www.youtube.com/watch?v=TSbjTC63Sck	https://www.youtube.com/watch?v=MIoXf4Q89q0	https://www.youtube.com/watch?v=7AFM5JeHwbM	https://www.youtube.com/watch?v=wRXDaquNDeQ	https://www.youtube.com/watch?v=vY4WPZ_mSYo	https://www.youtube.com/watch?v=xVisfqT8G2k	https://www.youtube.com/watch?v=-JB3JOfchCM	https://www.youtube.com/watch?v=Lj9LM1jfGs0	https://www.youtube.com/watch?v=Mg5OY2H_m1E	https://www.youtube.com/watch?v=SvXvUYVMh_o	https://www.youtube.com/watch?v=CcnuWgtPEsQ	https://www.youtube.com/watch?v=ZfqzU-GVUSk	https://www.youtube.com/watch?v=Ed9aORUlJtY	https://www.youtube.com/watch?v=LD6iiU_xuPQ
https://www.youtube.com/watch?v=VXUfhi5lF6U	https://www.youtube.com/watch?v=6cQsIrl72jY	https://www.youtube.com/watch?v=UL_cX38sAVE	https://www.youtube.com/watch?v=DvuHCyPn9dI	https://www.youtube.com/watch?v=GOzd_CklSLg	https://www.youtube.com/watch?v=2-bmAgak6-M	https://www.youtube.com/watch?v=FT0IxNW9ZBU	https://www.youtube.com/watch?v=qHUw7IaOOn0	https://www.youtube.com/watch?v=zcPmF01TqDc	https://www.youtube.com/watch?v=gS4-XtlVDMU	https://www.youtube.com/watch?v=S8IbOgv4gvY	https://www.youtube.com/watch?v=S5B6SHNXYuE	https://www.youtube.com/watch?v=X1J_OkRu0H8	https://www.youtube.com/watch?v=NDhftPAy4uU	https://www.youtube.com/watch?v=CwXXIzF8xfY	https://www.youtube.com/watch?v=c-f_2kr4K9E	https://www.youtube.com/watch?v=RC1Ui0tVsJA	N/A	https://www.youtube.com/watch?v=b7CPkx8vvvY	https://www.youtube.com/watch?v=vDD06sevb8g	N/A	https://www.youtube.com/watch?v=rARIL5EQQ1U	https://www.youtube.com/watch?v=3gfI4qciaQE	https://www.youtube.com/watch?v=zgfJ8QKdIzI	https://www.youtube.com/watch?v=za41VZDU9JA
https://www.youtube.com/watch?v=nr4MlWjyps8	https://www.youtube.com/watch?v=9cEhRffvgD8	https://www.youtube.com/watch?v=uERFNYxn0Bg	https://www.youtube.com/watch?v=_3_oJSopLHg	https://www.youtube.com/watch?v=y7ZGCFKDMVY	https://www.youtube.com/watch?v=oWPwudL2zx4	https://www.youtube.com/watch?v=Qn2kDwlb4_M	https://youtu.be/nr4MlWjyps8?t=91	https://www.youtube.com/watch?v=9Xmkl6LXUvg	https://youtu.be/nr4MlWjyps8?t=110	https://youtu.be/nr4MlWjyps8?t=120	https://www.youtube.com/watch?v=mBI_5g29-LA	https://www.youtube.com/watch?v=xdyhCZKgA5Q	https://youtu.be/nr4MlWjyps8?t=166	https://youtu.be/nr4MlWjyps8?t=180	https://www.youtube.com/watch?v=1QCn7WqWZEc	https://www.youtube.com/watch?v=_2gpZfQ-s0s	N/A	https://www.youtube.com/watch?v=w-6b5Cg06X4	https://youtu.be/nr4MlWjyps8?t=226	https://www.youtube.com/watch?v=JANL917rnzI	https://www.youtube.com/watch?v=kalcluHqFM0	https://youtu.be/nr4MlWjyps8?t=265	https://www.youtube.com/watch?v=IQ3-IO8LI1I	https://www.youtube.com/watch?v=zyimiMrj1mU
https://www.youtube.com/watch?v=8r0T4CCnQMI	https://www.youtube.com/watch?v=mFLGo4tJMNY	https://www.youtube.com/watch?v=Ex9U1SYiRYk	https://www.youtube.com/watch?v=XDLWTmuSQTs	https://www.youtube.com/watch?v=OG6Dzlq_2ms	https://www.youtube.com/watch?v=ccu5bF7i_Tk	https://www.youtube.com/watch?v=7udIr_VZ4ss	https://www.youtube.com/watch?v=QsPhqon9Mz4	https://www.youtube.com/watch?v=0JQH4MeKw0U	https://www.youtube.com/watch?v=3NexizuoWMc	https://www.youtube.com/watch?v=gyEHpOL8S1k	https://www.youtube.com/watch?v=jE7MbTCAoNw	https://www.youtube.com/watch?v=R4z4Kv47m3E	https://www.youtube.com/watch?v=DzSgZXABsvE	https://www.youtube.com/watch?v=5pUM25TJZOs	https://www.youtube.com/watch?v=DDT85MOsN-0	https://www.youtube.com/watch?v=80n8Fcc_ab4	N/A	https://www.youtube.com/watch?v=v_QItrMOidg	https://www.youtube.com/watch?v=wM6bWK1ao3g	N/A	https://www.youtube.com/watch?v=4XTUaYZZwDc	https://www.youtube.com/watch?v=1vv2-mmUCJU	https://www.youtube.com/watch?v=PAPA5Loj8FQ	https://www.youtube.com/watch?v=Z6pcPJcF0NU"""
    players_raw = """mudi	Samplay	Samplay	Hawk	Samplay	Samplay	jenkem66	Samplay	2 people	Samplay	Samplay	Hawk	Hawk	sockdude1	Samplay	Hawk	Samplay	1 target	Samplay	Samplay	9 targets	Samplay	Hawk	Samplay	Samplay
Jerry3333	LinksDarkArrows	Samplay	jenkem66	sockdude1	sockdude1	sockdude1	Jerry3333	2 people	sockdude1	Jerry3333	Jerry3333	sockdude1	Jerry3333	sockdude1	Jerry3333	sockdude1	Samplay	Samplay	Samplay	Samplay	Samplay	Jerry3333	sockdude1	Samplay
Samplay	Jerry3333	2 people	Samplay	Samplay	Samplay	Samplay	Samplay	Hawk	Samplay	Samplay	Samplay	Samplay	sockdude1	djwang88	Samplay	Samplay	1 target	Samplay	sockdude1	1221	Samplay	Samplay	Samplay	Samplay
Jerry3333	Jerry3333	Samplay	samthedigital	Jerry3333	9 targets	sockdude1	Jerry3333	Jerry3333	sockdude1	sockdude1	sockdude1	sockdude1	sockdude1	Jerry3333	sockdude1	sockdude1	1 target	sockdude1	Jerry3333	8 targets	Jerry3333	Jerry3333	sockdude1	Samplay
Bobby	Bobby	Samplay	Bobby	sockdude1	sockdude1	Bobby	Bobby	jenkem66	Bobby	Bobby	Bobby	Bobby	sockdude1	Samplay	Samplay	Bobby	sockdude1	Bobby	Bobby	Bobby	Bobby	Bobby	Bobby	Bobby
Samplay	Samplay	Samplay	sockdude1	sockdude1	3 people	sockdude1	sockdude1	sockdude1	Samplay	sockdude1	Samplay	sockdude1	sockdude1	sockdude1	djwang88	Samplay	1 target	Samplay	sockdude1	9 targets	Samplay	sockdude1	sockdude1	sockdude1
pokefantom	sockdude1	Samplay	jenkem66	sockdude1	9 targets	sockdude1	Jerry3333	pokefantom	sockdude1	sockdude1	Samplay	mimorox	sockdude1	Samplay	Samplay	Samplay	1 target	pokefantom	jenkem66	Samplay	Samplay	jenkem66	sockdude1	pokefantom
sockdude1	sockdude1	Samplay	jenkem66	sockdude1	Samplay	Bobby	samthedigital	mudi	sockdude1	sockdude1	sockdude1	sockdude1	jenkem66	mudi	sockdude1	jenkem66	jenkem66	sockdude1	sockdude1	9 targets	Samplay	sockdude1	sockdude1	sockdude1
9 targets	mimorox	Samplay	Bobby	sockdude1	jenkem66	sockdude1	megaqwertification	10 people	Bobby	sockdude1	sockdude1	mimorox	sockdude1	megaqwertification	megaqwertification	sockdude1	0 targets	mimorox	megaqwertification	8 targets	djwang88	Samplay	djwang88	djwang88
Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	8 people	Samplay	jenkem66	jenkem66	Samplay	Samplay	Samplay	Samplay	9 targets	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	sockdude1
jenkem66	jenkem66	jenkem66	jenkem66	jenkem66	jenkem66	jenkem66	jenkem66	2 people	jenkem66	mudi	jenkem66	jenkem66	jenkem66	jenkem66	jenkem66	jenkem66	9 targets	jenkem66	jenkem66	jenkem66	jenkem66	jenkem66	jenkem66	jenkem66
sockdude1	Jerry3333	Samplay	megaqwertification	megaqwertification	megaqwertification	1221	sockdude1	megaqwertification	Hawk	sockdude1	sockdude1	sockdude1	1221	sockdude1	pokefantom	sockdude1	6 targets	1221	sockdude1	Samplay	Samplay	megaqwertification	sockdude1	pokefantom
Samplay	sockdude1	Samplay	sockdude1	sockdude1	9 targets	sockdude1	sockdude1	sockdude1	Samplay	sockdude1	sockdude1	samthedigital	sockdude1	sockdude1	sockdude1	sockdude1	1 target	sockdude1	sockdude1	8 targets	sockdude1	sockdude1	sockdude1	sockdude1
Jerry3333	Jerry3333	Samplay	Jerry3333	Jerry3333	Jerry3333	Jerry3333	Samplay	Jerry3333	Samplay	Jerry3333	Jerry3333	mimorox	samthedigital	Jerry3333	Jerry3333	Jerry3333	1 target	mimorox	sockdude1	Jerry3333	Jerry3333	LinksDarkArrows	djwang88	Jerry3333
Samplay	Bobby	Samplay	Bobby	Bobby	Bobby	Bobby	Bobby	Bobby	Samplay	Bobby	Bobby	Bobby	Bobby	Mario 64 Master	Bobby	Bobby	Samplay	Samplay	Bobby	Bobby	Bobby	Bobby	Bobby	Bobby
Jerry3333	Samplay	Samplay	Jerry3333	Jerry3333	Jerry3333	Jerry3333	Jerry3333	Jerry3333	Jerry3333	Jerry3333	Jerry3333	Jerry3333	Jerry3333	Jerry3333	sockdude1	Jerry3333	Jerry3333	Jerry3333	sockdude1	sockdude1	Jerry3333	Jerry3333	Jerry3333	Jerry3333
Savestate	Savestate	Samplay	Savestate	Savestate	Savestate	Savestate	Savestate	Savestate	Savestate	Savestate	Savestate	Savestate	Savestate	Savestate	Savestate	samthedigital	Savestate	Savestate	Savestate	Savestate	Savestate	Savestate	Savestate	Savestate
Samplay	megaqwertification	Samplay	Jerry3333	Samplay	Samplay	megaqwertification	megaqwertification	LinksDarkArrows	megaqwertification	Samplay	Samplay	megaqwertification	Samplay	LinksDarkArrows	2 people	Samplay	megaqwertification	2 people	Samplay	Samplay	LinksDarkArrows	sockdude1	Samplay	Samplay
megaqwertification	pokefantom	Samplay	Judge9	pokefantom	LinksDarkArrows	megaqwertification	pokefantom	sockdude1	pokefantom	pokefantom	Samplay	mimorox	sockdude1	sockdude1	pokefantom	megaqwertification	Samplay	sockdude1	Samplay	Samplay	pokefantom	Samplay	sockdude1	pokefantom
Samplay	Samplay	Samplay	Samplay	Samplay	megaqwertification	Samplay	Samplay	LinksDarkArrows	Samplay	Samplay	Samplay	Samplay	LinksDarkArrows	Samplay	jenkem66	jenkem66	1 target	sockdude1	sockdude1	Samplay	Samplay	LinksDarkArrows	Samplay	jenkem66
Judge9	Judge9	Samplay	Judge9	Judge9	Judge9	Judge9	Judge9	Samplay	Samplay	Judge9	Judge9	Judge9	sockdude1	djwang88	megaqwertification	megaqwertification	Samplay	Judge9	Judge9	mudi	Samplay	1221	Judge9	1221
Samplay	Samplay	Samplay	Samplay	jenkem66	Samplay	Bobby	Samplay	2 people	Samplay	Samplay	Bobby	mimorox	Samplay	sockdude1	jenkem66	jenkem66	Samplay	jenkem66	Samplay	Samplay	3 people	jenkem66	Bobby	1221
Jerry3333	Jerry3333	Samplay	Samplay	Jerry3333	sockdude1	sockdude1	Jerry3333	megaqwertification	Samplay	sockdude1	Jerry3333	Hawk	Jerry3333	Jerry3333	Hawk	Jerry3333	1 target	Jerry3333	megaqwertification	9 targets	pokefantom	4 people	Jerry3333	pokefantom
Jerry3333	sockdude1	Samplay	Hawk	Hawk	jenkem66	jenkem66	Jerry3333	Jerry3333	Jerry3333	Jerry3333	Hawk	djwang88	Jerry3333	Jerry3333	djwang88	jenkem66	1 target	Samplay	Jerry3333	Jerry3333	Samplay	Jerry3333	sockdude1	Hawk
djwang88	sockdude1	Samplay	Samplay	sockdude1	djwang88	djwang88	djwang88	2 people	djwang88	djwang88	djwang88	djwang88	djwang88	djwang88	sockdude1	djwang88	1 target	sockdude1	djwang88	9 targets	2 people	LinksDarkArrows	djwang88	samthedigital"""
    frames = [line.split("\t") for line in frames_raw.split("\n")]
    videos = [line.split("\t") for line in videos_raw.split("\n")]
    players = [line.split("\t") for line in players_raw.split("\n")]
    for (char_index, (char_frames, char_videos, char_players)) in enumerate(
        zip(frames, videos, players)
    ):
        character = (
            session.query(Character).filter(Character.position == char_index).one()
        )
        for (stage_index, (frame_string, video_link, player_string)) in enumerate(
            zip(char_frames, char_videos, char_players)
        ):
            stage = session.query(Stage).filter(Stage.position == stage_index).one()
            try:
                player = get_player_by_name(player_string, session)
            except ValueError:
                player = None
            if "target" in player_string:
                time = None
                partial_targets = int(player_string[0])
            else:
                time = int(frame_string)
                partial_targets = None
            video_link = video_link if video_link != "N/A" else None
            add_record(
                session=session,
                character=character,
                stage=stage,
                player=player,
                time=time,
                partial_targets=partial_targets,
                video_link=video_link,
            )

    try:
        add_char_stage_alias(
            session=session,
            aliased_name="Mr. Game&Watch",
            known_name="Mr. Game & Watch",
        )
        add_char_stage_alias(
            session=session, aliased_name="Doc", known_name="Dr. Mario"
        )
        add_player_alias(session=session, aliased_name="Dr.M", known_name="Dr.M")
    except ValueError:
        pass

    ties_raw = """Luigi	3.21	samthedigital
		Samplay
Yoshi	7.21	sockdude1
		aMSa
		samthedigital
Ganon	4.7	LinksDarkArrows
		sockdude1
		Jerry3333
		chaos6
		mudi
		demon9
		moOonstermunch
		Freezard
		airr8897
		samthedigital
Falco	4.97	Zampa
		sockdude1
		mudi
		moOonstermunch
		marth1
		U3TY
		Hanky Panky
		LinksDarkArrows
Mewtwo	4.55	LinksDarkArrows
		Jerry3333
		samthedigital
Mr. Game&Watch	2.82	Zampa
		sockdude1
		Dr.M
		samthedigital
YL on Zelda	4.73	Jerry3333
		Samplay
Doc on Ganon	3.78	Ravenyte
		Hawk
Mario on Ganon	3.78	Ravenyte
		jenkem66
Fox on Seak	0.26	Zampa
		jenkem66
Roy on Ganon	3.63	Ravenyte
		djwang88
Mewtwo on Ganon	3.99	LinksDarkArrows
		Bobby
Fox on Ganon	3.78	LinksDarkArrows
		jenkem66
Roy on Mewtwo	4.95	Samplay
		megaqwertification
YL on Pichu	4.13	megaqwertification
		Samplay"""

    cur_combo = None
    for line in ties_raw.split("\n"):
        combo, _, player_string = line.split("\t")
        if combo and combo != cur_combo:
            cur_combo = combo
        if " on " in cur_combo:
            char_string, stage_string = cur_combo.split(" on ")
        else:
            char_string = stage_string = cur_combo
        character = get_character_by_name(char_string, session)
        stage = get_stage_by_name(stage_string, session)
        player = get_player_by_name(player_string, session)
        record = get_record(session=session, character=character, stage=stage)
        # skipping Seak records for now
        if not record:
            continue
        record.players.append(player)


def downgrade():
    pass
