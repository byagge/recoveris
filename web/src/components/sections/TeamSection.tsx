"use client";

import Image from "next/image";
import { useEffect, useRef } from "react";
import { AccordionArrow, LinkedInIcon } from "@/components/icons";
import { Button } from "@/components/ui/Button";
import { team } from "@/content/individuals";
import { site } from "@/content/site";
import type { Swiper as SwiperType } from "swiper";
import { Navigation } from "swiper/modules";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";

export function TeamSection() {
  const swiperRef = useRef<SwiperType | null>(null);
  const prevRef = useRef<HTMLAnchorElement>(null);
  const nextRef = useRef<HTMLAnchorElement>(null);

  useEffect(() => {
    const swiper = swiperRef.current;
    if (!swiper || !prevRef.current || !nextRef.current) return;
    if (typeof swiper.params.navigation !== "object") return;

    swiper.params.navigation.prevEl = prevRef.current;
    swiper.params.navigation.nextEl = nextRef.current;
    swiper.navigation.destroy();
    swiper.navigation.init();
    swiper.navigation.update();
  }, []);

  return (
    <section className="instructors">
      <div className="container">
        <div className="instructors-heading">
          <h2>
            {team.title} <span>{team.titleHighlight}</span>
          </h2>
          <div className="sub-title">{team.subtitle}</div>
        </div>

        <div className="about-slider" style={{ borderTop: "none" }}>
          <Swiper
            modules={[Navigation]}
            className="instructors-slider"
            spaceBetween={20}
            slidesPerView={1}
            breakpoints={{
              640: { slidesPerView: 1.2 },
              900: { slidesPerView: 2 },
              1200: { slidesPerView: 2.4 },
            }}
            onSwiper={(swiper) => {
              swiperRef.current = swiper;
            }}
          >
            {team.members.map((member) => (
              <SwiperSlide key={member.name} className="team-slide">
                <div className="slide-wrapper">
                  <div className="slide-img">
                    <Image
                      src={member.image}
                      alt={member.name}
                      width={206}
                      height={274}
                    />
                  </div>
                  <div className="slide-info">
                    <h3>{member.name}</h3>
                    <div className="slide-position">{member.position}</div>
                  </div>
                  <a
                    className="slide-linkedin"
                    href={member.linkedin}
                    target="_blank"
                    rel="noreferrer"
                    aria-label={`${member.name} LinkedIn`}
                  >
                    <LinkedInIcon />
                  </a>
                </div>
                <div className="slide-hover">
                  <p>{member.bio}</p>
                </div>
              </SwiperSlide>
            ))}
          </Swiper>

          <div className="team-slider-navigation">
            <a
              href="#team-prev"
              id="techteamSliderPrev"
              ref={prevRef}
              onClick={(e) => e.preventDefault()}
              aria-label="Previous"
            >
              <AccordionArrow />
            </a>
            <a
              href="#team-next"
              id="techteamSliderNext"
              ref={nextRef}
              onClick={(e) => e.preventDefault()}
              aria-label="Next"
            >
              <AccordionArrow />
            </a>
          </div>
        </div>

        <Button href={site.cta.href}>{site.cta.label}</Button>

        <div className="expert-leadership-webinars two-items">
          {team.videos.map((video) => (
            <div className="video-item" key={video.src}>
              <iframe
                width="100%"
                height="auto"
                src={video.src}
                title={video.title}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerPolicy="strict-origin-when-cross-origin"
                allowFullScreen
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
